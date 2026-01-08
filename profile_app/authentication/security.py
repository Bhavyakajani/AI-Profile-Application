from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
import logging

from profile_app.models.request_models import TokenData
from profile_app.config import config
from typing import Annotated


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
"""
oauth2_schema to get url from login route
"""

logger = logging.getLogger(__name__)

SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def create_access_token(data: dict):
    logger.debug("Creating access token")
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData | HTTPException | None:
    logger.debug("Authenticating User token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        return TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    return verify_token(token)
