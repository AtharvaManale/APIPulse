from pydantic import BaseModel, ConfigDict

class ApiInput(BaseModel):
    api_name: str
    url: str
    url_method: str
    url_headers: dict
    time_interval: int
    timeout: int
    expected_status_code: int

class APIResponse(BaseModel):
    api_name: str
    url: str
    url_method: str
    url_headers: dict
    time_interval: int
    timeout: int
    expected_status_code: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class APIUpdate(BaseModel):
    api_name: str | None = None
    url: str | None = None
    url_method: str | None = None
    url_headers: dict | None = None
    time_interval: int | None = None
    timeout: int | None = None
    expected_status_code: int | None = None
    is_active: bool | None = None