from pydantic import BaseModel

class ApiFetch(BaseModel):
    id: str

class ApiInput(BaseModel):
    api_name: str
    url: str
    url_method: str
    url_headers: dict
    time_interval: int
    timeout: int
    expected_status_code: int

class APIResponce(BaseModel):
    api_name: str
    url: str
    url_method: str
    url_headers: dict
    time_interval: int
    timeout: int
    expected_status_code: int
    is_active: bool