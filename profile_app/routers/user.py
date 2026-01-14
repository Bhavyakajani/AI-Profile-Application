from typing import Annotated, List, Literal
import logging
from fastapi import APIRouter, HTTPException, status, Response, Depends
from profile_app.database.dependencies import get_user_repository
from profile_app.database.repositories import UserRepository
from profile_app.models.response_models import (
    UserCreateResponse,
    UserRoleResponse,
    UserUpdateResponse,
    UserGetResponse,
)
from profile_app.models.request_models import  (
    User, 
    UserCreateRequest, 
    UserUpdateRequest
)
import profile_app.utils.app_util as util
from profile_app.authentication.security import get_current_user
from profile_app.services.user_service import UserService

router = APIRouter(
    prefix='/user',
    tags=['Users']
)
user_service = UserService()
logger = logging.getLogger(__name__)

@router.post('/register', response_model=UserCreateResponse)
async def create_user(
    user: UserCreateRequest,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    logger.debug(f"Received user creation request: \n{user.model_dump()}")
    if not user:
        raise HTTPException(status_code=402, detail='Bad Request: Invalid User Details')
    
    # Check if user already exists
    if await user_repo.exists_by_email(user.email):
        raise HTTPException(status_code=409, detail=f"User with email {user.email} already exists")
    
    user = User(**user.model_dump())
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
                status=new_user["status"],
                profiles=new_user.get("profiles", [])
            )
    
    raise HTTPException(status_code=400, detail="Failed to create user")

@router.get('/role-approval-list', status_code=status.HTTP_200_OK, response_model=List[UserRoleResponse])
async def get_users_awaiting_approval(
    current_user: Annotated[User, Depends(get_current_user)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    logger.info("Getting list of Users awaiting approval")
    logged_in_user = await user_repo.find_by_email(current_user.email)

    if not user_service.is_user_admin(logged_in_user):
        raise HTTPException(status_code=401, detail="Unauthorized access")

    users = await user_repo.find_by_status()
    user_list = [
        UserRoleResponse(
        id=str(user["_id"]), 
        name=user["name"],
        email=user["email"],
        role=user["role"],
        status=user["status"]
        ) for user in users
        ]
    return user_list

@router.patch('/{id}/role', status_code=status.HTTP_200_OK, response_model=UserRoleResponse)
async def update_user_role(
    id: str,
    role: Literal["admin", "client", "candidate"],
    current_user: Annotated[User, Depends(get_current_user)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    logger.info(f"Updating User role to: {role}")
    
    util.is_valid_objectId(id)
    
    logged_in_user = await user_repo.find_by_email(current_user.email)
    
    if not user_service.is_user_admin(logged_in_user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="You are not authorized. Please contact admin: admin@gmail.com")
    
    user = await user_repo.find_by_id(id)
    if user and not user_service.is_status_waiting(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="A role has already been assigned to the User")

    update_dict = {
        "role": role, 
        "status": "approved"
    }
    user = await user_repo.update_user(id, user_data=update_dict)
    if not user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail="Unable to update User role")
    return UserRoleResponse(
        id=str(user["_id"]), 
        name=user["name"],
        email=user["email"],
        role=user["role"],
        status=user["status"])



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    # Validate if id is of correct type ObjectId
    util.is_valid_objectId(id)
    logger.info(f"Deleting user with id: {id}")

    logged_in_user = await user_repo.find_by_email(current_user.email)
    
    if not user_service.is_user_admin(logged_in_user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Unauthorized access")  


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