from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class ChargerStatus(str, Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    FAULTED = "faulted"
    OFFLINE = "offline"


class SessionStatus(str, Enum):
    ACTIVE = "active"
    ENDED = "ended"

@dataclass(frozen=True)
class TelemetryReading:
    charger_id: str
    connector_id: str
    power_kw: float
    voltage: float
    current_amp: float
    measured_at: datetime
    error_code: str | None = None

    def has_fault(self) -> bool:
        return self.error_code is not None

@dataclass
class Connector:
    connector_id: str
    status: ChargerStatus = ChargerStatus.AVAILABLE
    latest_power_kw: float = 0.0

    def update_from_telemetry(self, telemetry: TelemetryReading) -> None:
        if telemetry.connector_id != self.connector_id:
            raise ValueError("Telemetry connector_id does not match connector")

        self.latest_power_kw = telemetry.power_kw

        if telemetry.has_fault():
            self.status = ChargerStatus.FAULTED
        elif telemetry.power_kw > 0:
            self.status = ChargerStatus.OCCUPIED
        else:
            self.status = ChargerStatus.AVAILABLE

@dataclass
class Charger:
    charger_id: str
    location_id: str
    connectors: list[Connector] = field(default_factory=list)
    status: ChargerStatus = ChargerStatus.AVAILABLE

    def get_connector(self, connector_id: str) -> Connector:
        for connector in self.connectors:
            if connector.connector_id == connector_id:
                return connector

        raise ValueError("Connector not found on charger")

    def apply_telemetry(self, telemetry: TelemetryReading) -> None:
        if telemetry.charger_id != self.charger_id:
            raise ValueError("Telemetry charger_id does not match charger")

        connector = self.get_connector(telemetry.connector_id)
        connector.update_from_telemetry(telemetry)

        if any(c.status == ChargerStatus.FAULTED for c in self.connectors):
            self.status = ChargerStatus.FAULTED
        elif any(c.status == ChargerStatus.OCCUPIED for c in self.connectors):
            self.status = ChargerStatus.OCCUPIED
        else:
            self.status = ChargerStatus.AVAILABLE

@dataclass
class ChargingSession:
    session_id: str
    charger_id: str
    connector_id: str
    started_at: datetime
    user_id: str | None = None
    contract_id: str | None = None
    status: SessionStatus = SessionStatus.ACTIVE
    ended_at: datetime | None = None
    energy_delivered_kwh: float = 0.0

    @classmethod
    def start(
        cls,
        charger_id: str,
        connector_id: str,
        user_id: str | None = None,
        contract_id: str | None = None,
    ) -> "ChargingSession":
        return cls(
            session_id=str(uuid4()),
            charger_id=charger_id,
            connector_id=connector_id,
            user_id=user_id,
            contract_id=contract_id,
            started_at=datetime.now(UTC),
        )

    def end(self, energy_delivered_kwh: float, ended_at: datetime | None = None) -> None:
        if self.status == SessionStatus.ENDED:
            raise ValueError("Charging session has already ended")

        if energy_delivered_kwh < 0:
            raise ValueError("Energy delivered cannot be negative")

        self.energy_delivered_kwh = energy_delivered_kwh
        self.ended_at = ended_at or datetime.now(UTC)
        self.status = SessionStatus.ENDED