import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel, Field

from app.application.use_cases import ChargingUseCases
from app.domain.models import Charger, ChargingSession
from app.infrastructure.memory_repository import (
    InMemoryChargerRepository,
    InMemoryChargingSessionRepository,
    InMemoryTelemetryRepository,
)

router = APIRouter()
logger = logging.getLogger("voltedge.api.charging")

charger_repository = InMemoryChargerRepository()
session_repository = InMemoryChargingSessionRepository()
telemetry_repository = InMemoryTelemetryRepository()

use_cases = ChargingUseCases(
    charger_repository=charger_repository,
    session_repository=session_repository,
    telemetry_repository=telemetry_repository,
)


class TelemetryRequest(BaseModel):
    charger_id: str = Field(min_length=1, examples=["charger-1"])
    connector_id: str = Field(min_length=1, examples=["connector-1"])
    power_kw: float = Field(ge=0, examples=[11.0])
    voltage: float = Field(ge=0, examples=[230.0])
    current_amp: float = Field(ge=0, examples=[16.0])
    error_code: str | None = Field(default=None, examples=["E-101"])


class StartSessionRequest(BaseModel):
    charger_id: str = Field(min_length=1, examples=["charger-1"])
    connector_id: str = Field(min_length=1, examples=["connector-1"])
    user_id: str | None = Field(default=None, examples=["user-1"])
    contract_id: str | None = Field(default=None, examples=["contract-1"])


class EndSessionRequest(BaseModel):
    energy_delivered_kwh: float = Field(ge=0, examples=[22.5])


class ConnectorResponse(BaseModel):
    connector_id: str
    status: str
    latest_power_kw: float


class ChargerResponse(BaseModel):
    charger_id: str
    location_id: str
    status: str
    connectors: list[ConnectorResponse]

    @classmethod
    def from_domain(cls, charger: Charger) -> "ChargerResponse":
        return cls(
            charger_id=charger.charger_id,
            location_id=charger.location_id,
            status=charger.status.value,
            connectors=[
                ConnectorResponse(
                    connector_id=connector.connector_id,
                    status=connector.status.value,
                    latest_power_kw=connector.latest_power_kw,
                )
                for connector in charger.connectors
            ],
        )


class ChargingSessionResponse(BaseModel):
    session_id: str
    charger_id: str
    connector_id: str
    user_id: str | None
    contract_id: str | None
    status: str
    started_at: datetime
    ended_at: datetime | None
    energy_delivered_kwh: float

    @classmethod
    def from_domain(cls, session: ChargingSession) -> "ChargingSessionResponse":
        return cls(
            session_id=session.session_id,
            charger_id=session.charger_id,
            connector_id=session.connector_id,
            user_id=session.user_id,
            contract_id=session.contract_id,
            status=session.status.value,
            started_at=session.started_at,
            ended_at=session.ended_at,
            energy_delivered_kwh=session.energy_delivered_kwh,
        )


@router.post("/telemetry", response_model=ChargerResponse)
def register_telemetry(request: TelemetryRequest):
    try:
        charger = use_cases.register_telemetry(
            charger_id=request.charger_id,
            connector_id=request.connector_id,
            power_kw=request.power_kw,
            voltage=request.voltage,
            current_amp=request.current_amp,
            error_code=request.error_code,
        )

        logger.info(
            "Telemetry registered charger_id=%s connector_id=%s power_kw=%s has_error=%s",
            request.charger_id,
            request.connector_id,
            request.power_kw,
            request.error_code is not None,
        )

        return ChargerResponse.from_domain(charger)

    except ValueError as error:
        logger.warning(
            "Telemetry registration failed charger_id=%s connector_id=%s reason=%s",
            request.charger_id,
            request.connector_id,
            str(error),
        )
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/sessions/start", response_model=ChargingSessionResponse)
def start_session(request: StartSessionRequest):
    try:
        session = use_cases.start_charging_session(
            charger_id=request.charger_id,
            connector_id=request.connector_id,
            user_id=request.user_id,
            contract_id=request.contract_id,
        )

        logger.info(
            "Charging session started session_id=%s charger_id=%s connector_id=%s",
            session.session_id,
            session.charger_id,
            session.connector_id,
        )

        return ChargingSessionResponse.from_domain(session)

    except ValueError as error:
        logger.warning(
            "Charging session start failed charger_id=%s connector_id=%s reason=%s",
            request.charger_id,
            request.connector_id,
            str(error),
        )
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/sessions/{session_id}/end", response_model=ChargingSessionResponse)
def end_session(
    request: EndSessionRequest,
    session_id: str = Path(min_length=1),
):
    try:
        session = use_cases.end_charging_session(
            session_id=session_id,
            energy_delivered_kwh=request.energy_delivered_kwh,
        )

        logger.info(
            "Charging session ended session_id=%s charger_id=%s energy_delivered_kwh=%s",
            session.session_id,
            session.charger_id,
            session.energy_delivered_kwh,
        )

        return ChargingSessionResponse.from_domain(session)

    except ValueError as error:
        logger.warning(
            "Charging session end failed session_id=%s reason=%s",
            session_id,
            str(error),
        )
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/chargers/{charger_id}/status", response_model=ChargerResponse)
def get_charger_status(charger_id: str = Path(min_length=1)):
    try:
        charger = use_cases.get_charger_status(charger_id)
        return ChargerResponse.from_domain(charger)

    except ValueError as error:
        logger.warning(
            "Charger status request failed charger_id=%s reason=%s",
            charger_id,
            str(error),
        )
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/sessions", response_model=list[ChargingSessionResponse])
def list_sessions():
    return [
        ChargingSessionResponse.from_domain(session)
        for session in use_cases.list_sessions()
    ]