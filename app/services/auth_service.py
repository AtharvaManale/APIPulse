from app.core.security import hash_password, verify_password, create_access_token
from sqlalchemy.orm import Session
from app.schemas.auth_schemas import RegistrationSchema
from app.repositories.users_repository import UsersRepository
from app.exceptions.auth_exceptions import (ExistingUserException,
                                            UserNotFoundException)
from app.models.users_model import Users

class AuthService:
    def register_user(db: Session, data: RegistrationSchema):
        user = UsersRepository.get_user_by_username(db, data.username)

        if user:
            raise ExistingUserException

        user = UsersRepository.get_user_by_email(db, data.email_id)

        if user:
            raise ExistingUserException
        
        new_user = Users(
            username = data.username,
            password = hash_password(data.password),
            email_id = data.email_id
        )
        try:
            UsersRepository.add_user(db, new_user)
            db.commit()
            db.refresh(user)
            return new_user

        except Exception:
            db.rollback()
            raise
