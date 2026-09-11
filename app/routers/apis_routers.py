from fastapi import Depends, APIRouter, HTTPException, status
from app.db.session import get_db
from app.dependencies.auth_dependency import get_current_user, Session
from app.models.users_model import Users
from app.services.api_service import APIServices
from app.exceptions.api_exceptions import APIException
from app.schemas.api_schemas import ApiFetch, APIResponce, ApiInput

apis = APIRouter(prefix="/api")

@apis.get('/{id}', response_class=APIResponce, status_code=status.HTTP_200_OK)
def get_api_by_id(id: ApiFetch, user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = user.id

    try:
        api = APIServices.api_info(db, id, user_id)

        return api

    except APIException as a:
        raise HTTPException(
            status_code=a.status_code,
            detail=a.message
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error."
        )


@apis.get("/all", response_class=list[APIResponce], status_code=status.HTTP_200_OK)
def get_all_apis_of_user(user: Users = Depends(get_current_user), db: Session=Depends(get_db)):
    user_id = user.id

    try:
        apis = APIServices.get_all_apis(db, user_id=user_id)

        return apis
    
    except APIException as a:
        raise HTTPException(
            status_code=a.status_code,
            detail=a.message
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error."
        )


@apis.post('/register',response_class=APIResponce, status_code=status.HTTP_201_CREATED)
def regiester_api(request: ApiInput, user: Users = Depends(get_current_user), db: Session=Depends(get_db)):
    user_id = user.id

    try:
        api = APIServices.register_api(db, request, user_id)

        return  api

    except APIException as a:
        raise HTTPException(
            status_code=a.status_code,
            detail=a.message
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error."
        )