from typing import List

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Response
from profile_app.dbManager import user_db
from profile_app.hashing import hash_password
from profile_app.models import UpdateUserResponse, User, ShowUser

router = APIRouter()
@router.post('/user', response_model=ShowUser, tags=['Users'])
def create_user(user: User):
    if user:
        user_dict = user.model_dump()
        user_dict = hash_password(user_dict)
        new_user = user_db.insert_user(user_dict)
        return ShowUser(name = user.name, email=user.email)
    else:
        raise HTTPException(status_code=402, detail='Bad Request: Invalid Profile Details')


@router.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Users'])
def delete_user(id, response: Response):
    if not ObjectId.is_valid(id):
        response.status_code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=400, detail="Invalid ObjectId")
    delete_result = user_db.delete_one(id)
    if delete_result.deleted_count == 1:
        return Response(status_code=204)
    raise HTTPException(status_code=404, detail=f"Profile {id} not found")

@router.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=ShowUser, tags=['Users'])
def get_user(id):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid User Id")
    user = user_db.find_by_id(id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    return ShowUser(name=user["name"], email=user["email"])

@router.patch('/user/{id}', response_model=UpdateUserResponse, tags=['Users'])
def update_user(id, user: User):
    oid_user = ObjectId(id)
    if not oid_user.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid User Id")
    user_dict = hash_password(user.model_dump())
    new_user = user_db.update_user(oid_user, user_dict)

    if new_user:
        new_user["_id"] = str(new_user["_id"])
        return UpdateUserResponse(message = f"User {id} updated successfully", updated_data = new_user)
    else:
        raise HTTPException(status_code=404, detail=f"Profile {id} not found")