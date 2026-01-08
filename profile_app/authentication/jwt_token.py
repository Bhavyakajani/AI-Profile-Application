from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException
from jwt import InvalidTokenError
import logging

from profile_app.models.request_models import TokenData
from profile_app.config import config

logger = logging.getLogger(__name__)

SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    logger.debug("Creating access token")
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception) -> TokenData | HTTPException | None:
    logger.debug("Authenticating User token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        return TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
