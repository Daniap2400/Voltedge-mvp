"""
Seeder PostgreSQL-databasen med eksisterende dummy data fra ML-datasættet.

Datasættet bruges som fælles datagrundlag for:
- ML / predictive maintenance
- database seed
- API analytics
- BI / Power BI

Kør inde i Docker:
    docker compose exec api python scripts/seed_database.py
"""

from csv import DictReader
from datetime import UTC, datetime, timedelta
from pathlib import Path

from app.domain.models import (
    Charger,
    ChargerStatus,
    ChargingSession,
    Connector,
    SessionStatus,
    TelemetryReading,
)
from app.infrastructure.database import SessionLocal, create_database
from app.infrastructure.sql_repository import (
    SqlChargerRepository,
    SqlChargingSessionRepository,
    SqlTelemetryRepository,
)


CSV_PATH = Path("/workspace/analytics/ml/data/charger_maintenance_sample.csv")


def resolve_csv_path() -> Path:
    if CSV_PATH.exists():
        return CSV_PATH

    raise FileNotFoundError(
        "Kunne ikke finde charger_maintenance_sample.csv på "
        "/workspace/analytics/ml/data/charger_maintenance_sample.csv. "
        "Kør først: python analytics/ml/generate_sample_data.py"
    )


def charger_status_from_row(row: dict) -> ChargerStatus:
    fault_count = int(row["fault_count_7d"])
    uptime = float(row["uptime_percentage"])
    maintenance_required = int(row["maintenance_required"])

    if maintenance_required == 1 or fault_count >= 3 or uptime < 97:
        return ChargerStatus.FAULTED

    return ChargerStatus.AVAILABLE


def parse_event_date(value: str) -> datetime:
    parsed_date = datetime.fromisoformat(value)

    if parsed_date.tzinfo is None:
        return parsed_date.replace(tzinfo=UTC)

    return parsed_date


def main() -> None:
    create_database()

    csv_path = resolve_csv_path()

    charger_repository = SqlChargerRepository(SessionLocal)
    session_repository = SqlChargingSessionRepository(SessionLocal)
    telemetry_repository = SqlTelemetryRepository(SessionLocal)

    with csv_path.open("r", encoding="utf-8") as file:
        rows = list(DictReader(file))

    unique_chargers: set[str] = set()

    for row in rows:
        charger_id = row["charger_id"]
        connector_id = "connector-1"
        event_date = parse_event_date(row["event_date"])

        status = charger_status_from_row(row)
        avg_power_kw = float(row["avg_power_kw"])
        total_sessions = max(1, int(row["total_sessions_7d"]))
        total_energy = float(row["total_energy_kwh_7d"])
        representative_energy = round(total_energy / total_sessions, 2)

        if charger_id not in unique_chargers:
            charger = Charger(
                charger_id=charger_id,
                location_id=row["location"].lower(),
                status=status,
                connectors=[
                    Connector(
                        connector_id=connector_id,
                        status=status,
                        latest_power_kw=avg_power_kw,
                    )
                ],
            )

            charger_repository.save(charger)
            unique_chargers.add(charger_id)

        telemetry_repository.save(
            TelemetryReading(
                charger_id=charger_id,
                connector_id=connector_id,
                power_kw=avg_power_kw,
                voltage=230.0,
                current_amp=round((avg_power_kw * 1000) / 230.0, 2),
                measured_at=event_date,
                error_code="MAINTENANCE_RISK"
                if int(row["maintenance_required"]) == 1
                else None,
            )
        )

        session_started = event_date + timedelta(hours=8)
        session_ended = session_started + timedelta(minutes=45)

        session_repository.save(
            ChargingSession(
                session_id=f"csv-{charger_id}-{row['event_date']}",
                charger_id=charger_id,
                connector_id=connector_id,
                user_id=f"user-{charger_id[-3:]}",
                contract_id=f"contract-{row['location'].lower()}",
                status=SessionStatus.ENDED,
                started_at=session_started,
                ended_at=session_ended,
                energy_delivered_kwh=representative_energy,
            )
        )

    print(f"Seeded database from: {csv_path}")
    print(f"Chargers created: {len(unique_chargers)}")
    print(f"Telemetry readings created: {len(rows)}")
    print(f"Charging sessions created: {len(rows)}")


if __name__ == "__main__":
    main()