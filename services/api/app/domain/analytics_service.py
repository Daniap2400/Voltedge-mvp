from dataclasses import dataclass

from app.domain.models import (
    Charger,
    ChargerStatus,
    ChargingSession,
    SessionStatus,
    TelemetryReading,
)


@dataclass(frozen=True)
class AnalyticsSummary:
    charger_count: int
    session_count: int
    ended_session_count: int
    total_energy_delivered_kwh: float
    average_session_duration_minutes: float
    utilization_rate: float
    charger_fault_rate: float
    expected_demand_kwh: float
    anomalies: list[str]


@dataclass(frozen=True)
class ChargerAnalytics:
    charger_id: str
    session_count: int
    total_energy_delivered_kwh: float
    average_session_duration_minutes: float
    fault_rate: float
    current_status: str
    anomalies: list[str]


class AnalyticsService:
    def create_summary(
        self,
        chargers: list[Charger],
        sessions: list[ChargingSession],
        telemetry_readings: list[TelemetryReading],
    ) -> AnalyticsSummary:
        ended_sessions = self._ended_sessions(sessions)

        return AnalyticsSummary(
            charger_count=len(chargers),
            session_count=len(sessions),
            ended_session_count=len(ended_sessions),
            total_energy_delivered_kwh=self.total_energy_delivered(ended_sessions),
            average_session_duration_minutes=self.average_session_duration(ended_sessions),
            utilization_rate=self.utilization_rate(chargers, sessions),
            charger_fault_rate=self.fault_rate(telemetry_readings),
            expected_demand_kwh=self.expected_demand(ended_sessions),
            anomalies=self.detect_energy_anomalies(ended_sessions),
        )

    def create_charger_analytics(
        self,
        charger: Charger,
        sessions: list[ChargingSession],
        telemetry_readings: list[TelemetryReading],
    ) -> ChargerAnalytics:
        charger_sessions = [
            session
            for session in sessions
            if session.charger_id == charger.charger_id
        ]
        ended_sessions = self._ended_sessions(charger_sessions)

        return ChargerAnalytics(
            charger_id=charger.charger_id,
            session_count=len(charger_sessions),
            total_energy_delivered_kwh=self.total_energy_delivered(ended_sessions),
            average_session_duration_minutes=self.average_session_duration(ended_sessions),
            fault_rate=self.fault_rate(telemetry_readings),
            current_status=charger.status.value,
            anomalies=self.detect_energy_anomalies(ended_sessions),
        )

    def total_energy_delivered(self, sessions: list[ChargingSession]) -> float:
        return round(
            sum(session.energy_delivered_kwh for session in sessions),
            2,
        )

    def average_session_duration(self, sessions: list[ChargingSession]) -> float:
        durations = [
            (session.ended_at - session.started_at).total_seconds() / 60
            for session in sessions
            if session.ended_at is not None
        ]

        if not durations:
            return 0.0

        return round(sum(durations) / len(durations), 2)

    def utilization_rate(
        self,
        chargers: list[Charger],
        sessions: list[ChargingSession],
    ) -> float:
        if not chargers:
            return 0.0

        occupied_chargers = {
            session.charger_id
            for session in sessions
            if session.status == SessionStatus.ACTIVE
        }

        return round((len(occupied_chargers) / len(chargers)) * 100, 2)

    def fault_rate(self, telemetry_readings: list[TelemetryReading]) -> float:
        if not telemetry_readings:
            return 0.0

        fault_count = sum(
            1
            for reading in telemetry_readings
            if reading.has_fault()
        )

        return round((fault_count / len(telemetry_readings)) * 100, 2)

    def expected_demand(self, sessions: list[ChargingSession]) -> float:
        if not sessions:
            return 0.0

        average_energy = self.total_energy_delivered(sessions) / len(sessions)

        return round(average_energy * len(sessions), 2)

    def detect_energy_anomalies(
        self,
        sessions: list[ChargingSession],
        threshold_kwh: float = 80.0,
    ) -> list[str]:
        anomalies = []

        for session in sessions:
            if session.energy_delivered_kwh > threshold_kwh:
                anomalies.append(
                    f"Session {session.session_id} has unusually high energy consumption: "
                    f"{session.energy_delivered_kwh} kWh"
                )

        return anomalies

    def _ended_sessions(
        self,
        sessions: list[ChargingSession],
    ) -> list[ChargingSession]:
        return [
            session
            for session in sessions
            if session.status == SessionStatus.ENDED
        ]