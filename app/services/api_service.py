from sqlalchemy.orm import Session
from app.models.apis_model import API
from app.models.users_model import Users
from app.repositories.apis_repository import ApiRepository
from app.schemas.api_schemas import ApiFetch, ApiInput
from app.exceptions.api_exceptions import (UserNotAuthorizedException,
                                           APINotFoundException, 
                                           ExistingEndpointException)

class APIServices:

    @staticmethod
    def api_info(db: Session, request: ApiFetch, user: Users):

        api = ApiRepository.get_api_by_id(db, api_id = request.id)

        if not api:
            raise APINotFoundException()

        if api.user_id == user.id:
            raise UserNotAuthorizedException()

        return api

    @staticmethod
    def get_all_apis(db: Session, request: ApiInput, user: Users):

        api = ApiRepository.get_api_by_url_url_method(db, request.url, request.url_method)

        if api:
            raise ExistingEndpointException()

        new_api = API(
            user_id = user.id,
            api_name = request.api_name,
            url = request.url,
            url_method = request.url_method,
            url_headers = request.url_headers,
            time_interval = request.time_interval,
            timeout = request.timeout,
            expected_status_code = request.expected_status_code
        )

        try:
            ApiRepository.register_endpoint(db, new_api)
            db.commit()
            db.refresh(new_api)

            return new_api

        except Exception:
            db.rollback()
            raise