from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from app.services.auth_service import AuthService, Session
from app.schemas.auth_schemas import RegistrationSchema, LoginSchema
from app.db.session import get_db
from app.exceptions.auth_exceptions import AuthException

auth = APIRouter(prefix="/auth")

@auth.post('/register')
def signup(request: RegistrationSchema, db: Session = Depends(get_db)):

    try:
        user, access_token = AuthService.register_user(db, request)

        return JSONResponse(content={"message" : "User Got Successfully registered",
                                    "user_id": user.id,
                                    "username": user.username,
                                    "email_id": user.email_id,
                                    "access_token": access_token,
                                    "token_type": "bearer"}, status_code=status.HTTP_201_CREATED)

    except AuthException as a:
        raise HTTPException(
            status_code=a.status_code,
            detail=a.message
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error, try later."
        )

@auth.post('/login')
def login(request: LoginSchema, db: Session = Depends(get_db)):

    try:
        access_token = AuthService.login_user(db, request)

        return JSONResponse(content={"message": "User is Authenticated",
                                    "access_token": access_token,
                                    "token_type": "bearer"}, status_code=status.HTTP_200_OK)

    except AuthException as a:
        raise HTTPException(
            status_code=a.status_code,
            detail=a.message
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error, try later."
        )