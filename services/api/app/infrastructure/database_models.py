from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base


class ChargerRow(Base):
    __tablename__ = "chargers"

    charger_id: Mapped[str] = mapped_column(String, primary_key=True)
    location_id: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)

    connectors: Mapped[list["ConnectorRow"]] = relationship(
        back_populates="charger",
        cascade="all, delete-orphan",
    )


class ConnectorRow(Base):
    __tablename__ = "connectors"

    connector_id: Mapped[str] = mapped_column(String, primary_key=True)
    charger_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("chargers.charger_id"),
        primary_key=True,
    )
    status: Mapped[str] = mapped_column(String, nullable=False)
    latest_power_kw: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    charger: Mapped[ChargerRow] = relationship(back_populates="connectors")


class ChargingSessionRow(Base):
    __tablename__ = "charging_sessions"

    session_id: Mapped[str] = mapped_column(String, primary_key=True)
    charger_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    connector_id: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[str | None] = mapped_column(String, nullable=True)
    contract_id: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    energy_delivered_kwh: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)


class TelemetryReadingRow(Base):
    __tablename__ = "telemetry_readings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    charger_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    connector_id: Mapped[str] = mapped_column(String, nullable=False)
    power_kw: Mapped[float] = mapped_column(Float, nullable=False)
    voltage: Mapped[float] = mapped_column(Float, nullable=False)
    current_amp: Mapped[float] = mapped_column(Float, nullable=False)
    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    error_code: Mapped[str | None] = mapped_column(String, nullable=True)