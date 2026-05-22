from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class DomainEvent:
    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True)
class ChargerTelemetryReceived(DomainEvent):
    charger_id: str = ""
    connector_id: str = ""
    power_kw: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ChargingSessionStarted(DomainEvent):
    session_id: str = ""
    charger_id: str = ""
    connector_id: str = ""


@dataclass(frozen=True)
class ChargingSessionEnded(DomainEvent):
    session_id: str = ""
    charger_id: str = ""
    connector_id: str = ""
    energy_delivered_kwh: float = 0.0


@dataclass(frozen=True)
class ChargerFaultDetected(DomainEvent):
    charger_id: str = ""
    connector_id: str = ""
    error_code: str = ""