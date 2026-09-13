from pydantic import BaseModel, ConfigDict
from datetime import datetime


class LogResponseSchema(BaseModel):
    api_id: str
    checked_at: datetime
    status_code: int
    latency_ms: int
    is_success: bool
    error_type: str | None=None
    error_message: str | None=None
    response_size: int | None=None

    model_config = ConfigDict(from_attributes=True)