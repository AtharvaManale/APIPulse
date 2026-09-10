from pwdlib import PasswordHash
import jwt
from app.core.config import settings
from datetime import datetime, timedelta, timezone

password_hash = PasswordHash.recommended()

def hash_password(password: str):
    return password_hash.hash(password=password)

def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)

def create_access_token(user_id: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        "sub": user_id,
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm = settings.jwt_algorithm
    )

def decode_access_token(token: str):
    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithm = settings.jwt_algorithm
    )