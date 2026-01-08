from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm


from profile_app.models.request_models import Token
from profile_app.database.dependencies import get_user_repository
from profile_app.database.repositories import UserRepository
from profile_app.authentication.security import create_access_token
from ..utils import app_util as util

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
async def login(
    request: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    user_dict = await user_repo.find_by_email(request.username)

    if not user_dict:
        raise HTTPException(status_code=404, detail=f"User with email {request.username} not found")
    
    if not util.verify_password(hashed_pwd=user_dict["password"], pwd=request.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # Generate JWT
    access_token = create_access_token(
        data={"sub": user_dict["email"]}
    )
    return Token(access_token=access_token, token_type="bearer")