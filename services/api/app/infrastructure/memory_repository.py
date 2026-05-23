from app.domain.models import Charger, ChargingSession, Connector, TelemetryReading


class InMemoryChargerRepository:
    def __init__(self) -> None:
        self._chargers: dict[str, Charger] = {
            "charger-1": Charger(
                charger_id="charger-1",
                location_id="location-1",
                connectors=[Connector(connector_id="connector-1")],
            )
        }

    def save(self, charger: Charger) -> None:
        self._chargers[charger.charger_id] = charger

    def get_by_id(self, charger_id: str) -> Charger | None:
        return self._chargers.get(charger_id)

    def list_all(self) -> list[Charger]:
        return list(self._chargers.values())


class InMemoryChargingSessionRepository:
    def __init__(self) -> None:
        self._sessions: dict[str, ChargingSession] = {}

    def save(self, session: ChargingSession) -> None:
        self._sessions[session.session_id] = session

    def get_by_id(self, session_id: str) -> ChargingSession | None:
        return self._sessions.get(session_id)

    def list_all(self) -> list[ChargingSession]:
        return list(self._sessions.values())


class InMemoryTelemetryRepository:
    def __init__(self) -> None:
        self._readings: list[TelemetryReading] = []

    def save(self, telemetry: TelemetryReading) -> None:
        self._readings.append(telemetry)

    def list_all(self) -> list[TelemetryReading]:
        return list(self._readings)

    def list_for_charger(self, charger_id: str) -> list[TelemetryReading]:
        return [
            reading
            for reading in self._readings
            if reading.charger_id == charger_id
        ]