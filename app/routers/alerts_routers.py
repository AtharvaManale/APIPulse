from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies.auth_dependency import get_current_user
from app.models.users_model import Users
from app.repositories.alerts_repository import AlertsRepository
from app.schemas.alerts_schemas import AlertResponse

alerts = APIRouter(prefix="/alerts", tags=["Alerts"])


@alerts.get("/all", response_model=list[AlertResponse], status_code=status.HTTP_200_OK)
def get_all_user_alerts(
    db: Session = Depends(get_db),
    user: Users = Depends(get_current_user),
):
    try:
        raw_alerts = AlertsRepository.get_alerts_by_user(db, user_id=user.id)
        result = []
        for a in raw_alerts:
            result.append(
                AlertResponse(
                    id=a.id,
                    api_id=a.api_id,
                    api_name=a.api.api_name if a.api else "Unknown API",
                    api_url=a.api.url if a.api else "",
                    api_method=a.api.url_method if a.api else "GET",
                    type=a.type,
                    message=a.message,
                    created_at=a.created_at,
                    resolved=a.resolved,
                    resolved_at=a.resolved_at,
                )
            )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch alert logs: {str(e)}"
        )
