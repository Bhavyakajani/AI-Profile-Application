from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Response, Depends, UploadFile

from profile_app.database.dependencies import get_profile_repository, get_user_repository
from profile_app.database.repositories import ProfileRepository, UserRepository
from profile_app.models.request_models import ProfileUpdateModel, TokenData, ProfileModel, User
from profile_app.models.response_models import ProfileResponse, ProfilesListResponse
from profile_app.services import user_service
import profile_app.utils.app_util as util
from profile_app.authentication.security import get_current_user
import profile_app.document_processing as dp
import logging
router = APIRouter(
    prefix='/profile',
    tags=['Profiles']
)

logger = logging.getLogger(__name__)

@router.get("/", response_model=ProfilesListResponse)
async def get_all_profiles(
    profile_repo: Annotated[ProfileRepository, Depends(get_profile_repository)]
):
    logger.info("Fetching all profiles")
    profiles = await profile_repo.find_all()
    total_count = await profile_repo.count()
    return ProfilesListResponse(total_count=total_count, profiles=profiles)



@router.post('/', response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile: ProfileModel,
    current_user: Annotated[User, Depends(get_current_user)],
    profile_repo: Annotated[ProfileRepository, Depends(get_profile_repository)], 
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    logged_in_user = await user_repo.find_by_email(current_user.email)

    if user_service.is_user_client(logged_in_user):
        raise HTTPException(status_code=401, detail="Unauthorized access")
    
    if await profile_repo.exists_by_name(profile.name or ""):
        raise HTTPException(status_code=409, detail=f"Profile with name {profile.name} already exists")
    
    profile.creator = current_user.email
    logger.debug("Creating a new profile")
    pid = await profile_repo.create(profile)
    
    if pid:
        new_profile = await profile_repo.find_by_id(pid)
        if new_profile:
            logger.info(f"Profile created with ID: {pid}")
            # Explicitly map _id to id to ensure proper serialization
            profile_dict = {k: v for k, v in new_profile.items() if k != "_id"}
            profile_dict["id"] = str(new_profile.get("_id", pid))
            return ProfileResponse(**profile_dict)
    
    raise HTTPException(status_code=400, detail="Failed to create profile")

@router.get('/search', status_code=200, response_model=ProfilesListResponse)
async def get_profiles_by_search(
    query: str,
    response: Response,
    profile_repo: Annotated[ProfileRepository, Depends(get_profile_repository)]
):
    # search_by_name is synchronous (uses PyMongo) so call it directly
    logger.info(f"Searching profiles with name: {query}")
    profiles = await profile_repo.search_profiles(query)
    # Validation
    if not profiles:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=404, detail=f"Profile with query: {query} not found")
    profiles = [ProfileResponse(**profile) for profile in profiles]
    return ProfilesListResponse(total_count=len(profiles), profiles=profiles)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile_by_id(
    id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    profile_repo: Annotated[ProfileRepository, Depends(get_profile_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    logged_in_user = await user_repo.find_by_email(current_user.email)
    
    if not user_service.is_user_admin(logged_in_user):
        raise HTTPException(status_code=401, detail="Unauthorized access")

    util.is_valid_objectId(id)
    logger.info(f"Deleting profile with id: {id}")
    if await profile_repo.delete(id):
        return Response(status_code=204)
    raise HTTPException(status_code=404, detail=f"Profile {id} not found")

@router.patch('/{id}', status_code=202)
async def update_profile(
    id: str,
    profile: ProfileUpdateModel,
    current_user: Annotated[User, Depends(get_current_user)],
    profile_repo: Annotated[ProfileRepository, Depends(get_profile_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    # Validate if id is of correct type ObjectId
    util.is_valid_objectId(id)

    logged_in_user = await user_repo.find_by_email(current_user.email)
    profile_dict  =await profile_repo.find_by_id(id)

    is_admin = user_service.is_user_admin(logged_in_user)
    is_owner = profile_dict["email"] == current_user.email
    if not (is_admin or is_owner):
        raise HTTPException(status_code=401, detail="Unauthorized access")

    logger.info(f"Updating profile with id: {id}")
    update_result = await profile_repo.update_profile(id, profile)

    if update_result:
        return {"message": f"Profile {id} updated successfully", "updated_data": update_result}
    else:
        raise HTTPException(status_code=404, detail=f"Profile {id} not found")

@router.get('/{id}', status_code=200, response_model=ProfileResponse)
async def get_profile_by_id(
    id: str,
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
    profile_repo: Annotated[ProfileRepository, Depends(get_profile_repository)]
):
    
    util.is_valid_objectId(id)
    logger.info("Fetching a specific profile")
    profile = await profile_repo.find_by_id(id)
    # Validation
    if profile is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=404, detail=f"Profile with id: {id} not found")
    # Explicitly map _id to id to ensure proper serialization
    profile_dict = {k: v for k, v in profile.items() if k != "_id"}
    profile_dict["id"] = str(profile.get("_id", id))
    return ProfileResponse(**profile_dict)


@router.post("/parse", response_model=ProfileResponse)
async def parse_profile(
    file: UploadFile,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    profile_repo: Annotated[ProfileRepository, Depends(get_profile_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    
    logged_in_user = await user_repo.find_by_email(current_user.email)

    if user_service.is_user_client(logged_in_user):
        raise HTTPException(status_code=401, detail="Unauthorized access")
    
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in ["pdf", "pptx", "jpg", "jpeg", "png"]:
        raise HTTPException(status_code=400, detail="File format not supported")
    logger.info("Saving uploaded file for parsing")
    file_path, stored_name, file_id = dp.save_upload_file_tmp(file)
    logger.info("Parsing Profile")
    profile_model = await util.parse_resume(file_path, current_user, profile_repo)
    if not profile_model:
        raise HTTPException(status_code=400, detail="Profile exists or an error might have occurred")
    return profile_model

