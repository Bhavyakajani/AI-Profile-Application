from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import profile_app.jwt_token as jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
"""
oauth2_schema to get url from login route
"""

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return jwt_token.verify_token(token, credentials_exception)
