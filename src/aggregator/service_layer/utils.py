from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends
from jose import jwt
from loguru import logger

from src.aggregator.setup import SECRET_KEY, ALGORITHM, oauth2_scheme


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    logger.info('Generated access token')
    return encoded_jwt


async def decode_access_token(access_token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except (jwt.JWTError, AttributeError):
        return None

    logger.info('Decoded access token')
    return username
