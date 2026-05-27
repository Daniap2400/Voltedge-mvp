import os

from app.infrastructure.database import SessionLocal, create_database
from app.infrastructure.memory_repository import (
    InMemoryChargerRepository,
    InMemoryChargingSessionRepository,
    InMemoryTelemetryRepository,
)
from app.infrastructure.sql_repository import (
    SqlChargerRepository,
    SqlChargingSessionRepository,
    SqlTelemetryRepository,
)


def create_repositories():
    """
    Uses in-memory repositories by default so unit/API tests stay simple.
    Uses SQL repositories when USE_DATABASE=true, for Docker/PostgreSQL runtime.
    """
    if os.getenv("USE_DATABASE", "false").lower() == "true":
        create_database()
        return (
            SqlChargerRepository(SessionLocal),
            SqlChargingSessionRepository(SessionLocal),
            SqlTelemetryRepository(SessionLocal),
        )

    return (
        InMemoryChargerRepository(),
        InMemoryChargingSessionRepository(),
        InMemoryTelemetryRepository(),
    )