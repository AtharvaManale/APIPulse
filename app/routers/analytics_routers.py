from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies.auth_dependency import get_current_user
from app.models.users_model import Users
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics_schemas import (
    APIMetricsResponse,
    LatencyTrendPoint,
    DashboardSummaryResponse,
    TimeWindow,
)
from app.exceptions.api_exceptions import APIException

analytics = APIRouter(prefix="/analytics",tags=["Analytics"])


@analytics.get('/{id}/metrics', response_model=APIMetricsResponse, status_code=status.HTTP_200_OK)
def get_api_metrics(
    id: str,
    window: TimeWindow = Query(default="24h", description="Time window: 24h, 7d, 30d"),
    db: Session = Depends(get_db),
    user: Users = Depends(get_current_user),
):
    try:
        return AnalyticsService.get_api_metrics(db, api_id=id, user_id=user.id, window=window)
    except APIException as a:
        raise HTTPException(status_code=a.status_code, detail=a.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error. {str(e)}")


@analytics.get('/{id}/trends', response_model=list[LatencyTrendPoint], status_code=status.HTTP_200_OK)
def get_api_latency_trends(

    id: str,
    window: TimeWindow = Query(default="24h", description="Time window: 24h, 7d, 30d"),
    limit: int = Query(default=200, ge=1, le=1000, description="Max trend points"),
    db: Session = Depends(get_db),
    user: Users = Depends(get_current_user),
):
    try:
        return AnalyticsService.get_api_trends(db, api_id=id, user_id=user.id, window=window, limit=limit)
    except APIException as a:
        raise HTTPException(status_code=a.status_code, detail=a.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error. {str(e)}")


@analytics.get('/dashboard/summary', response_model=DashboardSummaryResponse, status_code=status.HTTP_200_OK)
def get_dashboard_summary(
    window: TimeWindow = Query(default="24h", description="Time window: 24h, 7d, 30d"),
    db: Session = Depends(get_db),
    user: Users = Depends(get_current_user),
):
    try:
        return AnalyticsService.get_dashboard_summary(db, user_id=user.id, window=window)
    except APIException as a:
        raise HTTPException(status_code=a.status_code, detail=a.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error. {str(e)}")
