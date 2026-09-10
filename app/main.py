from fastapi import FastAPI
from app.routers.auth_apis import auth

app = FastAPI()
app.include_router(auth)

@app.get('/')
def health_check():
    return {'messsage' : 'Server is running'}