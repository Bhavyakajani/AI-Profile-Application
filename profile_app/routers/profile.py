from typing import List

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Response

from profile_app.dbManager import profile_db, user_db
from profile_app.models import ShowProfile, ProfileModel
import profile_app.utils.app_util as util

router = APIRouter(
    prefix='/profile',
    tags=['Profiles']
)


@router.get("/", response_model=List[ShowProfile])
def get_all_profiles():
    profiles = profile_db.find_all_profiles()
    return profiles

@router.post('/', response_model=ProfileModel, status_code=status.HTTP_201_CREATED)
def create_profile(profile: ProfileModel):
    if profile is None:
        raise HTTPException(status_code=402, detail='Bad Request: Invalid Profile Details')
    pid = profile_db.insert_profile(profile)
    if pid:
        return {"profile_id": pid}
    else:
        raise HTTPException(status_code=400)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_profile_by_id(id):
    # Validate if id is of correct type ObjectId
    util.is_valid_objectId(id)

    delete_result = profile_db.delete_one(id)
    if delete_result.deleted_count == 1:
        return Response(status_code=204)
    raise HTTPException(status_code=404, detail=f"Profile {id} not found")

@router.patch('/{id}', status_code=202)
def update_profile(id: str, profile: ProfileModel):
    # Validate if id is of correct type ObjectId
    util.is_valid_objectId(id)

    update_result = profile_db.update_profile(ObjectId(id), profile)

    if update_result:
        update_result["_id"] = str(update_result["_id"])
        return {"message": f"Profile {id} updated successfully", "updated_data": update_result}
    else:
        raise HTTPException(status_code=404, detail=f"Profile {id} not found")

@router.get('/{id}', status_code=200, response_model=ShowProfile)
def get_profile_by_id(id: str, response: Response):
    # Validate if id is of correct type ObjectId
    util.is_valid_objectId(id)

    profile = profile_db.find_by_id(pid=id)

    creator_id = profile.get("creator_id")
    creator = user_db.find_by_id(pid=creator_id)

    # Validation
    if profile is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=404, detail=f"Profile with id: {id} not found")
    if creator is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=404, detail=f"Creator with id: {creator_id} not found")

    return ShowProfile(creator=creator)