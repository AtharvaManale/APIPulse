from fastapi import FastAPI
import app.models  # noqa: F401
from app.routers.auth_routers import auth
from app.routers.apis_routers import apis
from app.routers.monitoring_routers import monitoring

app = FastAPI()
app.include_router(auth)
app.include_router(apis)
app.include_router(monitoring)

@app.get('/')
def health_check():
    return {'message': 'Server is running'}