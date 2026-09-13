from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.repositories.apis_repository import ApiRepository
from app.repositories.analytics_repository import AnalyticsRepository
from app.schemas.analytics_schemas import (
    APIMetricsResponse,
    LatencyMetrics,
    LatencyTrendPoint,
    DashboardSummaryResponse,
)
from app.exceptions.api_exceptions import APINotFoundException, UserNotAuthorizedException


class AnalyticsService:

    @staticmethod
    def _parse_window(window: str) -> datetime:
        now = datetime.now()
        if window == "7d":
            return now - timedelta(days=7)
        elif window == "30d":
            return now - timedelta(days=30)
        return now - timedelta(hours=24)

    @staticmethod
    def _calculate_percentile(sorted_values: list[int], p: float) -> float:
        if not sorted_values:
            return 0.0
        n = len(sorted_values)
        if n == 1:
            return float(sorted_values[0])
        k = (n - 1) * (p / 100.0)
        f = int(k)
        c = min(f + 1, n - 1)
        return round(sorted_values[f] + (sorted_values[c] - sorted_values[f]) * (k - f), 2)

    @staticmethod
    def _determine_health(latest_log) -> str:
        if not latest_log:
            return "no_data"
        if not latest_log.is_success or (latest_log.latency_ms is not None and latest_log.latency_ms > 500):
            return "down"
        if latest_log.latency_ms is not None and latest_log.latency_ms >= 200:
            return "degraded"
        return "healthy"

    @staticmethod
    def get_api_metrics(db: Session, api_id: str, user_id: str, window: str = "24h") -> APIMetricsResponse:
        api = ApiRepository.get_api_by_id(db, api_id)
        if not api:
            raise APINotFoundException()
        if api.user_id != user_id:
            raise UserNotAuthorizedException()

        since = AnalyticsService._parse_window(window)
        latencies = AnalyticsRepository.get_latencies_in_window(db, api_id, since)
        success_count, failure_count = AnalyticsRepository.get_success_failure_counts(db, api_id, since)
        status_distribution = AnalyticsRepository.get_status_code_distribution(db, api_id, since)
        latest_log = AnalyticsRepository.get_latest_log(db, api_id)

        total_checks = success_count + failure_count
        uptime_pct = round((success_count / total_checks) * 100, 2) if total_checks > 0 else 100.0

        if latencies:
            avg_lat = round(sum(latencies) / len(latencies), 2)
            min_lat = latencies[0]
            max_lat = latencies[-1]
            p50 = AnalyticsService._calculate_percentile(latencies, 50)
            p95 = AnalyticsService._calculate_percentile(latencies, 95)
            p99 = AnalyticsService._calculate_percentile(latencies, 99)
        else:
            avg_lat = 0.0
            min_lat = 0
            max_lat = 0
            p50 = 0.0
            p95 = 0.0
            p99 = 0.0

        current_health = AnalyticsService._determine_health(latest_log)

        return APIMetricsResponse(
            api_id=api.id,
            time_window=window,
            total_checks=total_checks,
            success_count=success_count,
            failure_count=failure_count,
            uptime_percentage=uptime_pct,
            latency=LatencyMetrics(
                avg_latency_ms=avg_lat,
                min_latency_ms=min_lat,
                max_latency_ms=max_lat,
                p50_latency_ms=p50,
                p95_latency_ms=p95,
                p99_latency_ms=p99
            ),
            status_code_distribution=status_distribution,
            current_health=current_health
        )

    @staticmethod
    def get_api_trends(db: Session, api_id: str, user_id: str, window: str = "24h", limit: int = 200) -> list[LatencyTrendPoint]:
        api = ApiRepository.get_api_by_id(db, api_id)
        if not api:
            raise APINotFoundException()
        if api.user_id != user_id:
            raise UserNotAuthorizedException()

        since = AnalyticsService._parse_window(window)
        logs = AnalyticsRepository.get_trend_logs(db, api_id, since, limit=limit)

        return [
            LatencyTrendPoint(
                timestamp=log.checked_at,
                latency_ms=log.latency_ms,
                is_success=log.is_success,
                status_code=log.status_code
            )
            for log in logs
        ]

    @staticmethod
    def get_dashboard_summary(db: Session, user_id: str, window: str = "24h") -> DashboardSummaryResponse:
        apis = ApiRepository.get_apis_of_user(db, user_id)
        total_apis = len(apis)

        if total_apis == 0:
            return DashboardSummaryResponse(
                total_apis=0,
                healthy_apis=0,
                degraded_apis=0,
                down_apis=0,
                overall_uptime_percentage=100.0,
                overall_avg_latency_ms=0.0
            )

        healthy = 0
        degraded = 0
        down = 0
        total_uptime_sum = 0.0
        total_avg_latency_sum = 0.0

        for api in apis:
            metrics = AnalyticsService.get_api_metrics(db, api.id, user_id, window)
            total_uptime_sum += metrics.uptime_percentage
            total_avg_latency_sum += metrics.latency.avg_latency_ms

            if metrics.current_health == "healthy":
                healthy += 1
            elif metrics.current_health == "degraded":
                degraded += 1
            elif metrics.current_health == "down":
                down += 1

        overall_uptime = round(total_uptime_sum / total_apis, 2)
        overall_avg_lat = round(total_avg_latency_sum / total_apis, 2)

        return DashboardSummaryResponse(
            total_apis=total_apis,
            healthy_apis=healthy,
            degraded_apis=degraded,
            down_apis=down,
            overall_uptime_percentage=overall_uptime,
            overall_avg_latency_ms=overall_avg_lat
        )
