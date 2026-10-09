from pydantic import BaseModel, ConfigDict
from datetime import datetime


class AlertResponse(BaseModel):
    id: int
    api_id: str
    api_name: str
    api_url: str
    api_method: str
    type: str
    message: str | None = None
    created_at: datetime
    resolved: bool
    resolved_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
