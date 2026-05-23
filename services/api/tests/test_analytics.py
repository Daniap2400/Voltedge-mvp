from datetime import UTC, datetime, timedelta

from app.domain.analytics_service import AnalyticsService
from app.domain.models import (
    Charger,
    ChargingSession,
    Connector,
    SessionStatus,
    TelemetryReading,
)


def test_analytics_summary_calculates_total_energy_and_duration():
    service = AnalyticsService()

    started_at = datetime.now(UTC) - timedelta(minutes=60)
    ended_at = datetime.now(UTC)

    session = ChargingSession(
        session_id="session-1",
        charger_id="charger-1",
        connector_id="connector-1",
        started_at=started_at,
        ended_at=ended_at,
        status=SessionStatus.ENDED,
        energy_delivered_kwh=22.5,
    )

    summary = service.create_summary(
        chargers=[
            Charger(
                charger_id="charger-1",
                location_id="location-1",
                connectors=[Connector(connector_id="connector-1")],
            )
        ],
        sessions=[session],
        telemetry_readings=[],
    )

    assert summary.total_energy_delivered_kwh == 22.5
    assert summary.average_session_duration_minutes == 60.0
    assert summary.ended_session_count == 1


def test_fault_rate_is_based_on_telemetry_errors():
    service = AnalyticsService()

    readings = [
        TelemetryReading(
            charger_id="charger-1",
            connector_id="connector-1",
            power_kw=11.0,
            voltage=230.0,
            current_amp=16.0,
            measured_at=datetime.now(UTC),
            error_code=None,
        ),
        TelemetryReading(
            charger_id="charger-1",
            connector_id="connector-1",
            power_kw=0.0,
            voltage=230.0,
            current_amp=0.0,
            measured_at=datetime.now(UTC),
            error_code="E-101",
        ),
    ]

    assert service.fault_rate(readings) == 50.0


def test_detects_unusual_energy_consumption():
    service = AnalyticsService()

    session = ChargingSession(
        session_id="session-high-energy",
        charger_id="charger-1",
        connector_id="connector-1",
        started_at=datetime.now(UTC) - timedelta(minutes=90),
        ended_at=datetime.now(UTC),
        status=SessionStatus.ENDED,
        energy_delivered_kwh=120.0,
    )

    anomalies = service.detect_energy_anomalies([session])

    assert len(anomalies) == 1
    assert "unusually high energy consumption" in anomalies[0]