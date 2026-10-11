from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.models
from app.core.config import settings
from app.routers.auth_routers import auth
from app.routers.apis_routers import apis
from app.routers.monitoring_routers import monitoring
from app.routers.analytics_routers import analytics
from app.routers.alerts_routers import alerts

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.external_url, settings.external_url_2],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth)
app.include_router(apis)
app.include_router(monitoring)
app.include_router(analytics)
app.include_router(alerts)


@app.get('/')
def health_check():
    return {'message': 'Server is running'}