from celery import Celery
from app.core.config import settings

celery = Celery(
    "APIPulse",
    broker= settings.redis_url,
    backend=settings.redis_url
)

celery.conf.timezone = "UTC"

celery.conf.imports = (
    "app.tasks.monitoring_tasks",
    "app.tasks.email_tasks",
)


celery.conf.beat_schedule = {
    "monitor-30-second-apis": {
        "task": "app.tasks.monitoring_tasks.monitor_apis_by_interval",
        "schedule": 30.0,
        "args": (30,),
    },

    "monitor-60-second-apis": {
        "task": "app.tasks.monitoring_tasks.monitor_apis_by_interval",
        "schedule": 60.0,
        "args": (60,),
    },

    "monitor-120-second-apis": {
        "task": "app.tasks.monitoring_tasks.monitor_apis_by_interval",
        "schedule": 120.0,
        "args": (120,),
    },

    "monitor-300-second-apis": {
        "task": "app.tasks.monitoring_tasks.monitor_apis_by_interval",
        "schedule": 300.0,
        "args": (300,),
    },
}