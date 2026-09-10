from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt

from app.db.session import get_db
from app.repositories.users_repository import UsersRepository
from app.core.security import decode_access_token
from app.exceptions.auth_exceptions import InvalidTokenException, UserNotFoundException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(db: Session = Depends(get_db), token: str=Depends(oauth2_scheme)):

    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")

        if not user_id:
            raise InvalidTokenException()

    except jwt.InvalidTokenError:
        raise InvalidTokenException()

    user = UsersRepository.get_user_by_id(db, user_id)

    if not user:
        raise UserNotFoundException()

    return user
