from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Response, Depends, UploadFile

from profile_app.database.dependencies import get_profile_repository
from profile_app.database.repositories import ProfileRepository
from profile_app.models.request_models import TokenData, ProfileModel, User
from profile_app.models.response_models import ProfileResponse, ProfilesListResponse
import profile_app.utils.app_util as util
from profile_app.authentication.oauth2 import get_current_user
import profile_app.document_processing as dp

router = APIRouter(
    prefix='/profile',
    tags=['Profiles']
)


@router.get("/", response_model=ProfilesListResponse)
async def get_all_profiles(
    profile_repo: Annotated[ProfileRepository, Depends(get_profile_repository)]
):
    profiles = await profile_repo.find_all()
    total_count = await profile_repo.count()
    return ProfilesListResponse(total_count=total_count, profiles=profiles)



@router.post('/', response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile: ProfileModel,
    current_user: Annotated[User, Depends(get_current_user)],
    profile_repo: Annotated[ProfileRepository, Depends(get_profile_repository)]
):
    if profile is None:
        raise HTTPException(status_code=402, detail='Bad Request: Invalid Profile Details')
    
    if await profile_repo.exists_by_name(profile.name or ""):
        raise HTTPException(status_code=409, detail=f"Profile with name {profile.name} already exists")
    
    profile.creator = current_user.email
    pid = await profile_repo.create(profile)
    
    if pid:
        new_profile = await profile_repo.find_by_id(pid)
        if new_profile:
            return ProfileResponse(**new_profile)
    
    raise HTTPException(status_code=400, detail="Failed to create profile")

@router.get('/search', status_code=200, response_model=ProfilesListResponse)
async def get_profile_by_name(
    query: str,
    response: Response,
    profile_repo: Annotated[ProfileRepository, Depends(get_profile_repository)]
):
    # search_by_name is synchronous (uses PyMongo) so call it directly
    profiles = await profile_repo.search_by_name(query)
    # Validation
    if not profiles:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=404, detail=f"Profile with name: {query} not found")
    profiles = [ProfileResponse(**profile) for profile in profiles]
    return ProfilesListResponse(total_count=len(profiles), profiles=profiles)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile_by_id(
    id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    profile_repo: Annotated[ProfileRepository, Depends(get_profile_repository)]
):
    # Validate if id is of correct type ObjectId
    util.is_valid_objectId(id)

    if await profile_repo.delete(id):
        return Response(status_code=204)
    raise HTTPException(status_code=404, detail=f"Profile {id} not found")

@router.patch('/{id}', status_code=202)
async def update_profile(
    id: str,
    profile: ProfileModel,
    current_user: Annotated[User, Depends(get_current_user)],
    profile_repo: Annotated[ProfileRepository, Depends(get_profile_repository)]
):
    # Validate if id is of correct type ObjectId
    util.is_valid_objectId(id)

    update_result = await profile_repo.update_profile(id, profile)

    if update_result:
        return {"message": f"Profile {id} updated successfully", "updated_data": update_result}
    else:
        raise HTTPException(status_code=404, detail=f"Profile {id} not found")

@router.get('/{id}', status_code=200, response_model=ProfileResponse)
def get_profile_by_id(
    id: str,
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
    profile_repo: Annotated[ProfileRepository, Depends(get_profile_repository)]
):
    # Validate if id is of correct type ObjectId
    util.is_valid_objectId(id)

    profile = profile_repo.find_by_id(id)
    # Validation
    if profile is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=404, detail=f"Profile with id: {id} not found")
    return ProfileResponse(**profile)


@router.post("/parse", response_model=ProfileResponse)
async def parse_profile(
    file: UploadFile,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    profile_repo: Annotated[ProfileRepository, Depends(get_profile_repository)]
):
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in ["pdf", "pptx", "jpg", "jpeg", "png"]:
        raise HTTPException(status_code=400, detail="File format not supported")

    file_path, stored_name, file_id = dp.save_upload_file_tmp(file)
    profile_model = util.parse_resume(file_path, current_user, profile_repo)
    if not profile_model:
        raise HTTPException(status_code=400, detail="Profile exists or an error might have occurred")
    return profile_model

