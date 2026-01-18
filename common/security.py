import jwt
from datetime import datetime, timedelta
from common.config import settings

ALGORITHM = "HS256"

def create_access_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)

def create_refresh_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=14)
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)

def decode_token(token: str):
    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[ALGORITHM]
    )
