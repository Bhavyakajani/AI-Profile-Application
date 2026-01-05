from typing import Annotated
import logging
from fastapi import APIRouter, HTTPException, status, Response, Depends
from profile_app.database.dependencies import get_user_repository
from profile_app.database.repositories import UserRepository
from profile_app.models.response_models import UserCreateResponse, UserUpdateResponse, UserGetResponse
from profile_app.models.request_models import  User, UserUpdateRequest
import profile_app.utils.app_util as util
from profile_app.authentication.oauth2 import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['Users']
)

logger = logging.getLogger(__name__)

@router.post('/', response_model=UserCreateResponse)
async def create_user(
    user: User,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    if not user:
        raise HTTPException(status_code=402, detail='Bad Request: Invalid User Details')
    
    # Check if user already exists
    if await user_repo.exists_by_email(user.email):
        raise HTTPException(status_code=409, detail=f"User with email {user.email} already exists")
    
    user_dict = user.model_dump()
    user_dict = util.hash_password(user_dict)
    logger.debug(f"Creating a new user... \n{user_dict}")
    new_user_id = await user_repo.create(user_dict)
    
    if new_user_id:
        new_user = await user_repo.find_by_id(new_user_id)
        if new_user:
            return UserCreateResponse(
                id=str(new_user["_id"]),
                name=new_user["name"],
                email=new_user["email"],
                role=new_user["role"],
                profiles=new_user.get("profiles", [])
            )
    
    raise HTTPException(status_code=400, detail="Failed to create user")


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    # Validate if id is of correct type ObjectId
    util.is_valid_objectId(id)
    logger.info(f"Deleting user with id: {id}")
    if await user_repo.delete(id):
        return Response(status_code=204)
    raise HTTPException(status_code=404, detail=f"User {id} not found")

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserCreateResponse)
async def get_user(
    id: str,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    # Validate if id is of correct type ObjectId
    util.is_valid_objectId(id)
    logger.info("Fetching a user")
    user = await user_repo.find_by_id(id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    
    return UserCreateResponse(
        id=str(user["_id"]),
        name=user["name"],
        email=user["email"],
        role=user["role"],
        profiles=user.get("profiles", [])
    )

@router.patch('/{id}', response_model=UserUpdateResponse)
async def update_user(
    id: str,
    user: UserUpdateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    # Validate if id is of correct type ObjectId
    util.is_valid_objectId(id)
    logger.debug(f"Patch request data: \n{user.model_dump()}")
    new_user = {
        k: v for k, v in user.model_dump(by_alias=True).items() if v is not None
    }
    
    if len(new_user) == 0:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    if user.password is not None:
        new_user = util.hash_password(new_user)

    updated_user = await user_repo.update_user(id, new_user)

    if updated_user:
        return UserUpdateResponse(
            message=f"User with id: {id} updated successfully",
            updated_data=UserGetResponse(
                id=updated_user["_id"],
                name=updated_user["name"],
                email=updated_user["email"],
                role=updated_user["role"]
            )
        )
    else:
        raise HTTPException(status_code=404, detail=f"User {id} not found")