from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm


from profile_app.models import Token
from profile_app.dbManager import user_db
from ..jwt_token import create_access_token
from ..utils import app_util as util

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
def login(request: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = user_db.get_db().find_one({"email": request.username})

    if not user_dict:
        raise HTTPException(status_code=404, detail=f"User with email {request.username} not found")
    if not util.verify_password(hashed_pwd=user_dict["password"], pwd=request.password):
        raise HTTPException(status_code=404, detail="Incorrect password")

    # Generate JWT
    access_token = create_access_token(
        data={"sub": user_dict["name"]}
    )
    return Token(access_token=access_token, token_type="bearer")