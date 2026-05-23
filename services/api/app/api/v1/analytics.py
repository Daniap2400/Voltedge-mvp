from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.application.use_cases import AnalyticsUseCases
from app.domain.analytics_service import AnalyticsService, AnalyticsSummary, ChargerAnalytics
from app.api.v1.charging import (
    charger_repository,
    session_repository,
    telemetry_repository,
)

router = APIRouter(prefix="/analytics")


analytics_use_cases = AnalyticsUseCases(
    charger_repository=charger_repository,
    session_repository=session_repository,
    telemetry_repository=telemetry_repository,
    analytics_service=AnalyticsService(),
)


class AnalyticsSummaryResponse(BaseModel):
    charger_count: int
    session_count: int
    ended_session_count: int
    total_energy_delivered_kwh: float
    average_session_duration_minutes: float
    utilization_rate: float
    charger_fault_rate: float
    expected_demand_kwh: float
    anomalies: list[str]

    @classmethod
    def from_domain(cls, summary: AnalyticsSummary) -> "AnalyticsSummaryResponse":
        return cls(
            charger_count=summary.charger_count,
            session_count=summary.session_count,
            ended_session_count=summary.ended_session_count,
            total_energy_delivered_kwh=summary.total_energy_delivered_kwh,
            average_session_duration_minutes=summary.average_session_duration_minutes,
            utilization_rate=summary.utilization_rate,
            charger_fault_rate=summary.charger_fault_rate,
            expected_demand_kwh=summary.expected_demand_kwh,
            anomalies=summary.anomalies,
        )


class ChargerAnalyticsResponse(BaseModel):
    charger_id: str
    session_count: int
    total_energy_delivered_kwh: float
    average_session_duration_minutes: float
    fault_rate: float
    current_status: str
    anomalies: list[str]

    @classmethod
    def from_domain(cls, analytics: ChargerAnalytics) -> "ChargerAnalyticsResponse":
        return cls(
            charger_id=analytics.charger_id,
            session_count=analytics.session_count,
            total_energy_delivered_kwh=analytics.total_energy_delivered_kwh,
            average_session_duration_minutes=analytics.average_session_duration_minutes,
            fault_rate=analytics.fault_rate,
            current_status=analytics.current_status,
            anomalies=analytics.anomalies,
        )


@router.get("/summary", response_model=AnalyticsSummaryResponse)
def get_analytics_summary():
    summary = analytics_use_cases.get_summary()
    return AnalyticsSummaryResponse.from_domain(summary)


@router.get("/chargers/{charger_id}", response_model=ChargerAnalyticsResponse)
def get_charger_analytics(charger_id: str):
    try:
        analytics = analytics_use_cases.get_charger_analytics(charger_id)
        return ChargerAnalyticsResponse.from_domain(analytics)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error