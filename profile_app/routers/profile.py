from typing import List, Annotated

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Response, Depends, UploadFile

from profile_app.database.dbManager import profile_db
from profile_app.models.request_models import TokenData, ProfileModel
from profile_app.models.response_models import ProfileResponse, ProfilesListResponse
from profile_app.schema import User
import profile_app.utils.app_util as util
from profile_app.authentication.oauth2 import get_current_user
import profile_app.document_processing as dp
router = APIRouter(
    prefix='/profile',
    tags=['Profiles']
)


@router.get("/", response_model=ProfilesListResponse)
def get_all_profiles():
    profiles = profile_db.find_all_profiles()
    total_count = profile_db.count_all_documents_in_collection()
    return ProfilesListResponse(total_count=total_count, profiles=profiles)



@router.post('/', response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(profile: ProfileModel, current_user: Annotated[User, Depends(get_current_user)]):
    print(profile)
    if profile is None:
        raise HTTPException(status_code=402, detail='Bad Request: Invalid Profile Details')
    if profile_db.profile_exists_by_name(profile.model_dump()):
        print(f"{profile} already exists")
        return None
    profile.creator = current_user.email
    pid = profile_db.insert_profile(profile)
    print(f"Profile Manually created with id: {pid}")
    if pid:
        new_profile = profile_db.find_by_id(pid)
        new_profile["_id"] = str(new_profile["_id"])
        return ProfileResponse(**new_profile)
    else:
        raise HTTPException(status_code=400)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_profile_by_id(id, current_user: Annotated[User, Depends(get_current_user)]):
    # Validate if id is of correct type ObjectId
    util.is_valid_objectId(id)

    delete_result = profile_db.delete_one(id)
    if delete_result.deleted_count == 1:
        return Response(status_code=204)
    raise HTTPException(status_code=404, detail=f"Profile {id} not found")

@router.patch('/{id}', status_code=202)
def update_profile(id: str, profile: ProfileModel, current_user: Annotated[User, Depends(get_current_user)]):
    # Validate if id is of correct type ObjectId
    util.is_valid_objectId(id)

    update_result = profile_db.update_profile(ObjectId(id), profile)

    if update_result:
        update_result["_id"] = str(update_result["_id"])
        return {"message": f"Profile {id} updated successfully", "updated_data": update_result}
    else:
        raise HTTPException(status_code=404, detail=f"Profile {id} not found")

@router.get('/{id}', status_code=200, response_model=ProfileResponse)
def get_profile_by_id(id: str, response: Response, current_user: Annotated[User, Depends(get_current_user)]):
    # Validate if id is of correct type ObjectId
    util.is_valid_objectId(id)

    profile = profile_db.find_by_id(pid=id)
    # Validation
    if profile is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=404, detail=f"Profile with id: {id} not found")
    profile["_id"] = str(profile["_id"])
    return ProfileResponse(**profile)


@router.post("/parse", response_model=ProfileResponse)
async def parse_profile(file: UploadFile, current_user: Annotated[TokenData, Depends(get_current_user)]):
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in ["pdf", "pptx", "jpg", "jpeg", "png"]:
        raise HTTPException(status_code=400, detail="File format not supported")

    file_path, stored_name, file_id = dp.save_upload_file_tmp(file)
    profile_model = util.parse_resume(file_path, current_user)
    if not profile_model :
        return HTTPException(status_code=400, detail="Profile exists or an error might have occurred")
    return profile_model

@router.get('/search', status_code=200, response_model=ProfilesListResponse)
async def get_profile_by_name(query: str, response: Response, current_user: Annotated[User, Depends(get_current_user)]):
    # Validate if id is of correct type ObjectId
    profiles = await profile_db.search_user_by_name(name=query)
    # Validation
    if not profiles:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=404, detail=f"Profile with name: {query} not found")
    profiles = [ProfileResponse(**profile) for profile in profiles]
    return ProfilesListResponse(total_count=len(profiles), profiles=profiles)
