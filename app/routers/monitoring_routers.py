from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.db.session import get_db
from app.dependencies.auth_dependency import get_current_user, Session
from app.models.users_model import Users
from app.services.monitoring_service import MonitoringService
from app.schemas.logs_schemas import LogResponseSchema
from app.exceptions.api_exceptions import APIException


monitoring = APIRouter(prefix='/check')

@monitoring.get('/{id}', status_code=status.HTTP_201_CREATED, response_model=LogResponseSchema)
def check_api(id: str, db: Session = Depends(get_db), user: Users = Depends(get_current_user)):

    try:
        log = MonitoringService.monitor_api_endpoint(db, id, user.id)

        return log

    except APIException as a:
        raise HTTPException(
            status_code=a.status_code,
            detail=a.message
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error."
        )

@monitoring.get('/{id}/logs', status_code=status.HTTP_200_OK, response_model=list[LogResponseSchema])
def get_logs(id: str, db: Session = Depends(get_db), user: Users = Depends(get_current_user)):

    try:
        logs = MonitoringService.get_logs(db, id,user.id)

        return logs
    
    except APIException as a:
        raise HTTPException(
            status_code=a.status_code,
            detail=a.message
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error."
        )

@monitoring.get('/{id}/recent_log', status_code=status.HTTP_200_OK, response_model=LogResponseSchema)
def get_last_log(id: str, db: Session = Depends(get_db), user: Users = Depends(get_current_user)):

    try:
        recent_log = MonitoringService.get_last_log(db, id, user.id)

        return recent_log
    
    except APIException as a:
        raise HTTPException(
            status_code=a.status_code,
            detail=a.message
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error."
        )