from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends
from jose import jwt
from loguru import logger

from src.setup import oauth2_scheme, settings


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.encryption.secret_key, algorithm=settings.encryption.algorithm)

    logger.info('Generated access token')
    return encoded_jwt


async def decode_access_token(access_token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(access_token, settings.encryption.secret_key, algorithms=[settings.encryption.algorithm])
        username: str = payload.get("sub")
        if username is None:
            return None
    except (jwt.JWTError, AttributeError):
        return None

    logger.info('Decoded access token')
    return username
