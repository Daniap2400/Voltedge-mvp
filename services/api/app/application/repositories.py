from typing import Protocol

from app.domain.models import Charger, ChargingSession, TelemetryReading


class ChargerRepository(Protocol):
    def save(self, charger: Charger) -> None:
        ...

    def get_by_id(self, charger_id: str) -> Charger | None:
        ...

    def list_all(self) -> list[Charger]:
        ...


class ChargingSessionRepository(Protocol):
    def save(self, session: ChargingSession) -> None:
        ...

    def get_by_id(self, session_id: str) -> ChargingSession | None:
        ...

    def list_all(self) -> list[ChargingSession]:
        ...


class TelemetryRepository(Protocol):
    def save(self, telemetry: TelemetryReading) -> None:
        ...

    def list_all(self) -> list[TelemetryReading]:
        ...

    def list_for_charger(self, charger_id: str) -> list[TelemetryReading]:
        ...