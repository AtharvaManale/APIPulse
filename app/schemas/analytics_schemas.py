from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict

TimeWindow = Literal["24h", "7d", "30d"]

class LatencyMetrics(BaseModel):
    avg_latency_ms: float
    min_latency_ms: int
    max_latency_ms: int
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float

class APIMetricsResponse(BaseModel):
    api_id: str
    time_window: str
    total_checks: int
    success_count: int
    failure_count: int
    uptime_percentage: float
    latency: LatencyMetrics
    status_code_distribution: dict[str, int]
    current_health: str

    model_config = ConfigDict(from_attributes=True)

class LatencyTrendPoint(BaseModel):
    timestamp: datetime
    latency_ms: int | None = None
    is_success: bool
    status_code: int | None = None

    model_config = ConfigDict(from_attributes=True)

class DashboardSummaryResponse(BaseModel):
    total_apis: int
    healthy_apis: int
    degraded_apis: int
    down_apis: int
    overall_uptime_percentage: float
    overall_avg_latency_ms: float
