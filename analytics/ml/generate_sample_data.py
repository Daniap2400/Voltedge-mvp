from pathlib import Path
import csv
import random
from datetime import datetime, timedelta


OUTPUT_PATH = Path(__file__).parent / "data" / "charger_maintenance_sample.csv"
random.seed(42)


def calculate_maintenance_required(
    fault_count_7d: int,
    offline_minutes_7d: int,
    failed_sessions_7d: int,
    uptime_percentage: float,
    anomaly_count_7d: int,
    days_since_last_maintenance: int,
    firmware_age_days: int,
) -> int:
    """
    Rule used to label synthetic data.

    1 = maintenance required / elevated risk
    0 = normal risk

    This is not the ML model itself.
    This only creates a realistic target variable for the training dataset.
    """
    risk_score = 0

    if fault_count_7d >= 3:
        risk_score += 2

    if offline_minutes_7d >= 90:
        risk_score += 2

    if failed_sessions_7d >= 5:
        risk_score += 2

    if uptime_percentage < 97:
        risk_score += 2

    if anomaly_count_7d >= 3:
        risk_score += 1

    if days_since_last_maintenance >= 120:
        risk_score += 1

    if firmware_age_days >= 240:
        risk_score += 1

    return 1 if risk_score >= 4 else 0


def generate_rows(row_count: int = 1000) -> list[dict]:
    rows = []
    start_date = datetime.now() - timedelta(days=180)

    locations = ["Copenhagen", "Aarhus", "Odense", "Aalborg", "Roskilde"]
    charger_models = ["VE-AC-22", "VE-DC-50", "VE-DC-150"]
    firmware_versions = ["1.0.2", "1.1.0", "1.2.4", "2.0.1"]

    for index in range(1, row_count + 1):
        charger_number = random.randint(1, 120)
        charger_id = f"charger-{charger_number:03d}"

        fault_count_7d = random.choices(
            population=[0, 1, 2, 3, 4, 5, 6, 7, 8],
            weights=[34, 24, 15, 10, 7, 4, 3, 2, 1],
        )[0]

        offline_minutes_7d = max(0, int(random.gauss(25 + fault_count_7d * 35, 35)))
        failed_sessions_7d = max(0, int(random.gauss(fault_count_7d * 1.8, 2)))
        anomaly_count_7d = max(0, int(random.gauss(fault_count_7d * 1.2, 1.5)))

        uptime_percentage = round(
            max(85.0, min(100.0, 100 - (offline_minutes_7d / 10080 * 100))),
            2,
        )

        avg_power_kw = round(random.uniform(3.5, 22.0), 2)
        total_sessions_7d = random.randint(10, 220)
        total_energy_kwh_7d = round(total_sessions_7d * avg_power_kw * random.uniform(0.25, 1.4), 2)

        days_since_last_maintenance = random.randint(1, 180)
        firmware_age_days = random.randint(1, 365)
        temperature_avg_c = round(random.uniform(-8, 28), 1)

        maintenance_required = calculate_maintenance_required(
            fault_count_7d=fault_count_7d,
            offline_minutes_7d=offline_minutes_7d,
            failed_sessions_7d=failed_sessions_7d,
            uptime_percentage=uptime_percentage,
            anomaly_count_7d=anomaly_count_7d,
            days_since_last_maintenance=days_since_last_maintenance,
            firmware_age_days=firmware_age_days,
        )

        event_date = start_date + timedelta(days=random.randint(0, 180))

        rows.append(
            {
                "event_date": event_date.date().isoformat(),
                "charger_id": charger_id,
                "location": random.choice(locations),
                "charger_model": random.choice(charger_models),
                "firmware_version": random.choice(firmware_versions),
                "avg_power_kw": avg_power_kw,
                "total_sessions_7d": total_sessions_7d,
                "total_energy_kwh_7d": total_energy_kwh_7d,
                "fault_count_7d": fault_count_7d,
                "offline_minutes_7d": offline_minutes_7d,
                "failed_sessions_7d": failed_sessions_7d,
                "uptime_percentage": uptime_percentage,
                "anomaly_count_7d": anomaly_count_7d,
                "days_since_last_maintenance": days_since_last_maintenance,
                "firmware_age_days": firmware_age_days,
                "temperature_avg_c": temperature_avg_c,
                "maintenance_required": maintenance_required,
            }
        )

    return rows


def main() -> None:
    rows = generate_rows(row_count=1000)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows")
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()