from datetime import datetime, timedelta
from jose import jwt, JWTError
from core.config import settings
from typing import Optional

ALGORITHM = settings.JWT_ALGORITHM
SECRET_KEY = settings.JWT_SECRET_KEY

def create_access_token(user_id: int, role: str, expires_minutes: Optional[int] = None) -> str:
    expire = datetime.utcnow() + timedelta(minutes=(expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"sub": str(user_id), "role": role, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: int, expires_days: Optional[int] = None) -> str:
    expire = datetime.utcnow() + timedelta(days=(expires_days or settings.REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode = {"sub": str(user_id), "type": "refresh", "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise Exception(e)
