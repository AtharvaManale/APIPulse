from sqlalchemy.orm import Session
from app.models.apis_model import API
from app.models.users_model import Users
from app.repositories.apis_repository import ApiRepository
from app.schemas.api_schemas import ApiInput, APIUpdate
from app.exceptions.api_exceptions import (UserNotAuthorizedException,
                                           APINotFoundException, 
                                           ExistingEndpointException,
                                           NoAPIRegisteredException)

class APIServices:

    @staticmethod
    def api_info(db: Session, id: str, user_id: str) -> API:

        api = ApiRepository.get_api_by_id(db, api_id = id)

        if not api:
            raise APINotFoundException()

        if api.user_id != user_id:
            raise UserNotAuthorizedException()

        return api


    @staticmethod
    def get_all_apis(db: Session, user_id: str):

        apis = ApiRepository.get_apis_of_user(db, user_id)

        if len(apis) == 0:
            raise NoAPIRegisteredException()
        
        return apis


    @staticmethod
    def register_api(db: Session, request: ApiInput, user_id: str) -> API:

        api = ApiRepository.get_api_by_url_url_method(db, request.url, request.url_method)

        if api:
            raise ExistingEndpointException()

        new_api = API(
            user_id = user_id,
            api_name = request.api_name,
            url = request.url,
            url_method = request.url_method,
            url_headers = request.url_headers,
            time_interval = request.time_interval,
            timeout = request.timeout,
            expected_status_code = request.expected_status_code,
            is_active = request.is_active
        )

        try:
            ApiRepository.register_endpoint(db, new_api)
            db.commit()
            db.refresh(new_api)

            return new_api

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()


    @staticmethod
    def update_api_endpoint(db: Session, request: APIUpdate, user_id: str, api_id: str):
        api = ApiRepository.get_api_by_id(db, api_id)

        if not api:
            raise APINotFoundException()
        
        if api.user_id != user_id:
            raise UserNotAuthorizedException()

        other_api = ApiRepository.get_api_by_url_url_method(db, request.url, request.url_method)

        if other_api:
            raise ExistingEndpointException()

        updates = request.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(api, field, value)

        try:
            db.commit()
            db.refresh(api)

            return api
        
        except Exception:
            db.rollback()
            raise

        finally:
            db.close()


    @staticmethod
    def delete_api(db: Session, api_id: str, user_id: str):

        api = ApiRepository.get_api_by_id(db, api_id = api_id)
        
        if not api:
            raise APINotFoundException()
        
        if api.user_id != user_id:
            raise UserNotAuthorizedException()

        try:
            ApiRepository.delete_endpoint(db, api)
            db.commit()

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    @staticmethod
    def toggle_active_status(db: Session, api_id: str, user_id: str, is_active: bool | None = None) -> API:
        api = ApiRepository.get_api_by_id(db, api_id=api_id)

        if not api:
            raise APINotFoundException()

        if api.user_id != user_id:
            raise UserNotAuthorizedException()

        if is_active is None:
            api.is_active = not api.is_active
        else:
            api.is_active = is_active

        try:
            db.commit()
            db.refresh(api)
            return api
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
