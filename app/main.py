from fastapi import FastAPI
from app.routers.auth_routers import auth
from app.routers.apis_routers import apis

app = FastAPI()
app.include_router(auth)
app.include_router(apis)

@app.get('/')
def health_check():
    return {'messsage' : 'Server is running'}