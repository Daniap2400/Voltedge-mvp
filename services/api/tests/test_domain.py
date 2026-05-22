from datetime import UTC, datetime

import pytest

from app.domain import (
    Charger,
    ChargerFaultDetected,
    ChargerStatus,
    ChargingSession,
    Connector,
    SessionStatus,
    TelemetryReading,
)


def test_charger_updates_connector_from_telemetry() -> None:
    charger = Charger(
        charger_id="charger-1",
        location_id="location-1",
        connectors=[Connector(connector_id="connector-1")],
    )

    telemetry = TelemetryReading(
        charger_id="charger-1",
        connector_id="connector-1",
        power_kw=11.0,
        voltage=230.0,
        current_amp=16.0,
        measured_at=datetime.now(UTC),
    )

    charger.apply_telemetry(telemetry)

    assert charger.status == ChargerStatus.OCCUPIED
    assert charger.get_connector("connector-1").latest_power_kw == 11.0


def test_charger_fault_is_detected_from_telemetry() -> None:
    charger = Charger(
        charger_id="charger-1",
        location_id="location-1",
        connectors=[Connector(connector_id="connector-1")],
    )

    telemetry = TelemetryReading(
        charger_id="charger-1",
        connector_id="connector-1",
        power_kw=0.0,
        voltage=0.0,
        current_amp=0.0,
        measured_at=datetime.now(UTC),
        error_code="E-101",
    )

    charger.apply_telemetry(telemetry)

    assert charger.status == ChargerStatus.FAULTED
    assert charger.get_connector("connector-1").status == ChargerStatus.FAULTED


def test_charging_session_can_be_started_and_ended() -> None:
    session = ChargingSession.start(
        charger_id="charger-1",
        connector_id="connector-1",
        user_id="user-1",
    )

    session.end(energy_delivered_kwh=22.5)

    assert session.status == SessionStatus.ENDED
    assert session.energy_delivered_kwh == 22.5
    assert session.ended_at is not None


def test_charging_session_cannot_end_twice() -> None:
    session = ChargingSession.start(
        charger_id="charger-1",
        connector_id="connector-1",
    )

    session.end(energy_delivered_kwh=10.0)

    with pytest.raises(ValueError):
        session.end(energy_delivered_kwh=12.0)


def test_domain_event_contains_business_fact() -> None:
    event = ChargerFaultDetected(
        charger_id="charger-1",
        connector_id="connector-1",
        error_code="E-101",
    )

    assert event.charger_id == "charger-1"
    assert event.connector_id == "connector-1"
    assert event.error_code == "E-101"
    assert event.event_id
    assert event.occurred_at