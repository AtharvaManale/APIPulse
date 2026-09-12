from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.db.session import get_db
from app.dependencies.auth_dependency import get_current_user, Session
from app.models.users_model import Users
from app.services.api_service import APIServices
from app.exceptions.api_exceptions import APIException
from app.schemas.api_schemas import APIResponse, ApiInput, APIUpdate

apis = APIRouter(prefix="/api")

@apis.get('/{id}', response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_api_by_id(id: str, user: Users = Depends(get_current_user), db: Session = Depends(get_db)):

    try:
        api = APIServices.api_info(db, id, user.id)

        return api

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


@apis.get("/all", response_model=list[APIResponse], status_code=status.HTTP_200_OK)
def get_all_apis_of_user(user: Users = Depends(get_current_user), db: Session=Depends(get_db)):

    try:
        apis = APIServices.get_all_apis(db, user_id=user.id)

        return apis
    
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


@apis.post('/register',response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def regiester_api(request: ApiInput, user: Users = Depends(get_current_user), db: Session=Depends(get_db)):

    try:
        api = APIServices.register_api(db, request, user.id)

        return  api

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


@apis.patch('/update/{id}', response_model= APIResponse, status_code=status.HTTP_202_ACCEPTED)
def update_api_endpoint(id: str, request: APIUpdate, db: Session = Depends(get_db), user: Users = Depends(get_current_user)):

    try:
        api = APIServices.update_api_endpoint(db, request, user.id, id)

        return api
    
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


@apis.delete('/delete/{id}')
def delete_api_endpoint(id: str, db: Session = Depends(get_db), user: Users = Depends(get_current_user)):

    try:
        APIServices.delete_api(db, id, user.id)

        return JSONResponse(content={"message": "API endpoint deleted successfully."}, status_code=status.HTTP_200_OK)

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