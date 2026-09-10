from app.core.security import hash_password, verify_password, create_access_token
from sqlalchemy.orm import Session
from app.schemas.auth_schemas import RegistrationSchema, LoginSchema
from app.repositories.users_repository import UsersRepository
from app.exceptions.auth_exceptions import (ExistingUserException,
                                            ExistingEmailException,
                                            UserNotFoundException,
                                            UserNotAuthenticatedException)
from app.models.users_model import Users

class AuthService:

    @staticmethod
    def register_user(db: Session, request: RegistrationSchema):
        user = UsersRepository.get_user_by_username(db, request.username)

        if user:
            raise ExistingUserException()

        email = UsersRepository.get_user_by_email(db, request.email_id)

        if email:
            raise ExistingEmailException()
        
        new_user = Users(
            username = request.username,
            password = hash_password(request.password),
            email_id = request.email_id
        )
        try:
            UsersRepository.add_user(db, new_user)
            db.commit()
            db.refresh(new_user)

            access_token = create_access_token(user_id=user.id)

            return new_user, access_token

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def login_user(db: Session, request: LoginSchema):
        user = UsersRepository.get_user_by_username(db, request.username)
        
        if not user:
            raise UserNotFoundException()

        if not verify_password(request.password, user.password):
            raise UserNotAuthenticatedException()

        access_token = create_access_token(user_id=user.id)

        return access_token