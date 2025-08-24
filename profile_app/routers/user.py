from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Response, Depends
from profile_app.database.dbManager import user_db
from profile_app.schema import UpdateUserResponse, User, ShowUser
import profile_app.utils.app_util as util
from profile_app.authentication.oauth2 import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['Users']
)
@router.post('/', response_model=ShowUser)
def create_user(user: User):
    if user:
        user_dict = user.model_dump()
        user_dict = util.hash_password(user_dict)
        new_user = user_db.insert_user(user_dict)
        return ShowUser(name = user.name, email=user.email)
    else:
        raise HTTPException(status_code=402, detail='Bad Request: Invalid Profile Details')


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id, current_user: Annotated[User, Depends(get_current_user)]):

    # Validate if id is of correct type ObjectId
    util.is_valid_objectId(id)
    delete_result = user_db.delete_one(id)
    if delete_result.deleted_count == 1:
        return Response(status_code=204)
    raise HTTPException(status_code=404, detail=f"Profile {id} not found")

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ShowUser)
def get_user(id):
    # Validate if id is of correct type ObjectId
    util.is_valid_objectId(id)
    user = user_db.find_by_id(id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    return ShowUser(name=user["name"], email=user["user_name"])

@router.patch('/{id}', response_model=UpdateUserResponse)
def update_user(id, user: User, current_user: Annotated[User, Depends(get_current_user)]):
    oid_user = ObjectId(id)
    # Validate if id is of correct type ObjectId
    util.is_valid_objectId(oid_user)
    user_dict = util.hash_password(user.model_dump())
    new_user = user_db.update_user(oid_user, user_dict)

    if new_user:
        new_user["_id"] = str(new_user["_id"])
        return UpdateUserResponse(message = f"User {id} updated successfully", updated_data = new_user)
    else:
        raise HTTPException(status_code=404, detail=f"Profile {id} not found")