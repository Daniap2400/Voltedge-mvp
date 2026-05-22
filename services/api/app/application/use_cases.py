from datetime import UTC, datetime

from app.application.repositories import (
    ChargerRepository,
    ChargingSessionRepository,
    TelemetryRepository,
)
from app.domain.models import (
    Charger,
    ChargerStatus,
    ChargingSession,
    Connector,
    TelemetryReading,
)


class ChargingUseCases:
    def __init__(
        self,
        charger_repository: ChargerRepository,
        session_repository: ChargingSessionRepository,
        telemetry_repository: TelemetryRepository,
    ) -> None:
        self.charger_repository = charger_repository
        self.session_repository = session_repository
        self.telemetry_repository = telemetry_repository

    def register_telemetry(
        self,
        charger_id: str,
        connector_id: str,
        power_kw: float,
        voltage: float,
        current_amp: float,
        error_code: str | None = None,
    ) -> Charger:
        charger = self._get_or_create_charger(charger_id, connector_id)

        telemetry = TelemetryReading(
            charger_id=charger_id,
            connector_id=connector_id,
            power_kw=power_kw,
            voltage=voltage,
            current_amp=current_amp,
            measured_at=datetime.now(UTC),
            error_code=error_code,
        )

        charger.apply_telemetry(telemetry)

        self.telemetry_repository.save(telemetry)
        self.charger_repository.save(charger)

        return charger

    def start_charging_session(
        self,
        charger_id: str,
        connector_id: str,
        user_id: str | None = None,
        contract_id: str | None = None,
    ) -> ChargingSession:
        charger = self._get_or_create_charger(charger_id, connector_id)
        connector = charger.get_connector(connector_id)

        if connector.status == ChargerStatus.FAULTED:
            raise ValueError("Cannot start session on a faulted connector")

        session = ChargingSession.start(
            charger_id=charger_id,
            connector_id=connector_id,
            user_id=user_id,
            contract_id=contract_id,
        )

        connector.status = ChargerStatus.OCCUPIED
        charger.status = ChargerStatus.OCCUPIED

        self.session_repository.save(session)
        self.charger_repository.save(charger)

        return session

    def end_charging_session(
        self,
        session_id: str,
        energy_delivered_kwh: float,
    ) -> ChargingSession:
        session = self.session_repository.get_by_id(session_id)

        if session is None:
            raise ValueError("Charging session not found")

        session.end(energy_delivered_kwh=energy_delivered_kwh)

        charger = self.charger_repository.get_by_id(session.charger_id)
        if charger is not None:
            connector = charger.get_connector(session.connector_id)
            connector.status = ChargerStatus.AVAILABLE
            connector.latest_power_kw = 0.0
            charger.status = ChargerStatus.AVAILABLE
            self.charger_repository.save(charger)

        self.session_repository.save(session)

        return session

    def get_charger_status(self, charger_id: str) -> Charger:
        charger = self.charger_repository.get_by_id(charger_id)

        if charger is None:
            raise ValueError("Charger not found")

        return charger

    def list_sessions(self) -> list[ChargingSession]:
        return self.session_repository.list_all()

    def _get_or_create_charger(self, charger_id: str, connector_id: str) -> Charger:
        charger = self.charger_repository.get_by_id(charger_id)

        if charger is None:
            charger = Charger(
                charger_id=charger_id,
                location_id="unknown",
                connectors=[Connector(connector_id=connector_id)],
            )
            self.charger_repository.save(charger)

        return charger