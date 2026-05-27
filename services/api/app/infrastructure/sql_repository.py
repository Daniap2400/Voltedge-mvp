from collections.abc import Callable

from sqlalchemy.orm import Session, selectinload

from app.domain.models import (
    Charger,
    ChargerStatus,
    ChargingSession,
    Connector,
    SessionStatus,
    TelemetryReading,
)
from app.infrastructure.database_models import (
    ChargerRow,
    ChargingSessionRow,
    ConnectorRow,
    TelemetryReadingRow,
)

SessionFactory = Callable[[], Session]


class SqlChargerRepository:
    def __init__(self, session_factory: SessionFactory) -> None:
        self.session_factory = session_factory

    def save(self, charger: Charger) -> None:
        with self.session_factory() as session:
            row = session.get(ChargerRow, charger.charger_id)
            if row is None:
                row = ChargerRow(charger_id=charger.charger_id)
                session.add(row)

            row.location_id = charger.location_id
            row.status = charger.status.value
            row.connectors.clear()
            row.connectors.extend(
                ConnectorRow(
                    charger_id=charger.charger_id,
                    connector_id=connector.connector_id,
                    status=connector.status.value,
                    latest_power_kw=connector.latest_power_kw,
                )
                for connector in charger.connectors
            )
            session.commit()

    def get_by_id(self, charger_id: str) -> Charger | None:
        with self.session_factory() as session:
            row = session.get(
                ChargerRow,
                charger_id,
                options=[selectinload(ChargerRow.connectors)],
            )
            return _charger_from_row(row) if row else None

    def list_all(self) -> list[Charger]:
        with self.session_factory() as session:
            rows = (
                session.query(ChargerRow)
                .options(selectinload(ChargerRow.connectors))
                .all()
            )
            return [_charger_from_row(row) for row in rows]


class SqlChargingSessionRepository:
    def __init__(self, session_factory: SessionFactory) -> None:
        self.session_factory = session_factory

    def save(self, charging_session: ChargingSession) -> None:
        with self.session_factory() as session:
            row = session.get(ChargingSessionRow, charging_session.session_id)
            if row is None:
                row = ChargingSessionRow(session_id=charging_session.session_id)
                session.add(row)

            row.charger_id = charging_session.charger_id
            row.connector_id = charging_session.connector_id
            row.user_id = charging_session.user_id
            row.contract_id = charging_session.contract_id
            row.status = charging_session.status.value
            row.started_at = charging_session.started_at
            row.ended_at = charging_session.ended_at
            row.energy_delivered_kwh = charging_session.energy_delivered_kwh
            session.commit()

    def get_by_id(self, session_id: str) -> ChargingSession | None:
        with self.session_factory() as session:
            row = session.get(ChargingSessionRow, session_id)
            return _charging_session_from_row(row) if row else None

    def list_all(self) -> list[ChargingSession]:
        with self.session_factory() as session:
            rows = session.query(ChargingSessionRow).all()
            return [_charging_session_from_row(row) for row in rows]


class SqlTelemetryRepository:
    def __init__(self, session_factory: SessionFactory) -> None:
        self.session_factory = session_factory

    def save(self, telemetry: TelemetryReading) -> None:
        with self.session_factory() as session:
            session.add(
                TelemetryReadingRow(
                    charger_id=telemetry.charger_id,
                    connector_id=telemetry.connector_id,
                    power_kw=telemetry.power_kw,
                    voltage=telemetry.voltage,
                    current_amp=telemetry.current_amp,
                    measured_at=telemetry.measured_at,
                    error_code=telemetry.error_code,
                )
            )
            session.commit()

    def list_all(self) -> list[TelemetryReading]:
        with self.session_factory() as session:
            rows = session.query(TelemetryReadingRow).all()
            return [_telemetry_from_row(row) for row in rows]

    def list_for_charger(self, charger_id: str) -> list[TelemetryReading]:
        with self.session_factory() as session:
            rows = (
                session.query(TelemetryReadingRow)
                .filter(TelemetryReadingRow.charger_id == charger_id)
                .all()
            )
            return [_telemetry_from_row(row) for row in rows]


def _charger_from_row(row: ChargerRow) -> Charger:
    return Charger(
        charger_id=row.charger_id,
        location_id=row.location_id,
        status=ChargerStatus(row.status),
        connectors=[
            Connector(
                connector_id=connector.connector_id,
                status=ChargerStatus(connector.status),
                latest_power_kw=connector.latest_power_kw,
            )
            for connector in row.connectors
        ],
    )


def _charging_session_from_row(row: ChargingSessionRow) -> ChargingSession:
    return ChargingSession(
        session_id=row.session_id,
        charger_id=row.charger_id,
        connector_id=row.connector_id,
        user_id=row.user_id,
        contract_id=row.contract_id,
        status=SessionStatus(row.status),
        started_at=row.started_at,
        ended_at=row.ended_at,
        energy_delivered_kwh=row.energy_delivered_kwh,
    )


def _telemetry_from_row(row: TelemetryReadingRow) -> TelemetryReading:
    return TelemetryReading(
        charger_id=row.charger_id,
        connector_id=row.connector_id,
        power_kw=row.power_kw,
        voltage=row.voltage,
        current_amp=row.current_amp,
        measured_at=row.measured_at,
        error_code=row.error_code,
    )