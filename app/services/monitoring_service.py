from datetime import datetime
import time
import httpx

from sqlalchemy.orm import Session
from app.models.monitored_logs_model import MonitoredLogs
from app.models.apis_model import API
from app.repositories.logs_repository import LogsRepository
from app.repositories.apis_repository import ApiRepository
from app.exceptions.api_exceptions import (APINotFoundException,
                                           UserNotAuthorizedException)
from app.services.alerts_service import AlertsService


class MonitoringService:

    @staticmethod
    def get_logs(db: Session, api_id: str, user_id: str):
        api = ApiRepository.get_api_by_id(db, api_id)

        if not api:
            raise APINotFoundException()

        if api.user_id != user_id:
            raise UserNotAuthorizedException()

        logs = LogsRepository.get_logs_of_api(db, api_id)

        return logs

    @staticmethod
    def get_last_log(db: Session, api_id:str, user_id: str):
        api = ApiRepository.get_api_by_id(db, api_id)

        if not api:
            raise APINotFoundException()

        if api.user_id != user_id:
            raise UserNotAuthorizedException()

        recent_log = LogsRepository.get_recent_logof_api(db, api_id)

        return recent_log

    @staticmethod
    def monitor_api_endpoint(db: Session, api_id: str, user_id: str):
        api = ApiRepository.get_api_by_id(db, api_id)
        
        if not api:
            raise APINotFoundException()

        if api.user_id != user_id:
            raise UserNotAuthorizedException()

        try:
            checked_at = datetime.now()
            start_time = time.perf_counter()
            
            with httpx.Client(
                timeout=api.timeout,
                follow_redirects=True
            ) as client:
                response = client.request(
                    method=api.url_method,
                    url=api.url,
                    headers=api.url_headers
                )

            end_time = time.perf_counter()

            response_time_ms = int((end_time - start_time) * 1000)

            is_success = (api.expected_status_code == response.status_code)

            if is_success:
                error_type = None
                error_message = None
            else:
                reason = response.reason_phrase or "Unknown"
                if 500 <= response.status_code < 600:
                    error_type = "HTTP 5xx Server Error"
                elif 400 <= response.status_code < 500:
                    error_type = "HTTP 4xx Client Error"
                else:
                    error_type = "Status Code Mismatch"
                
                error_message = f"Expected HTTP {api.expected_status_code}, received HTTP {response.status_code} ({reason})"

            log = MonitoredLogs(
                api_id = api.id,
                checked_at = checked_at,
                status_code = response.status_code,
                latency_ms = response_time_ms,
                is_success = is_success,
                error_type = error_type,
                error_message = error_message,
                response_size = len(response.content)
            )

        except httpx.TimeoutException:
            end_time = time.perf_counter()
            response_time_ms = int((end_time - start_time) * 1000)

            log = MonitoredLogs(
                api_id = api.id,
                checked_at = checked_at,
                status_code = None,
                latency_ms = response_time_ms,
                is_success = False,
                error_type = "Timeout Error",
                error_message = f"Request timed out after {api.timeout}s",
                response_size = 0
            )

        except httpx.ConnectError as e:
            end_time = time.perf_counter()
            response_time_ms = int((end_time - start_time) * 1000)

            log = MonitoredLogs(
                api_id = api.id,
                checked_at = checked_at,
                status_code = None,
                latency_ms = response_time_ms,
                is_success = False,
                error_type = "Connection Error",
                error_message = f"Connection failed: {str(e)}",
                response_size = 0
            )

        except httpx.RequestError as e:
            end_time = time.perf_counter()
            response_time_ms = int((end_time - start_time) * 1000)

            log = MonitoredLogs(
                api_id = api.id,
                checked_at = checked_at,
                status_code = None,
                latency_ms = response_time_ms,
                is_success = False,
                error_type = "Network Error",
                error_message = f"Request error: {str(e)}",
                response_size = 0
            )

        except Exception as e:
            end_time = time.perf_counter()
            response_time_ms = int((end_time - start_time) * 1000) if 'start_time' in locals() else 0

            log = MonitoredLogs(
                api_id = api.id,
                checked_at = checked_at if 'checked_at' in locals() else datetime.now(),
                status_code = None,
                latency_ms = response_time_ms,
                is_success = False,
                error_type = "Probe Execution Error",
                error_message = f"Probe failed: {str(e)}",
                response_size = 0
            )

        LogsRepository.add_log(db, log)
        db.commit()
        db.refresh(log)

        AlertsService.evaluate_probe(db, api, log)
        return log
