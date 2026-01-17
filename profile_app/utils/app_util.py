from typing import Any, Optional

from bson import ObjectId
from fastapi import HTTPException
import profile_app.ai.llm_model as llm

from passlib.context import CryptContext

from profile_app.models.request_models import ProfileModel
from profile_app.models.response_models import ProfileResponse
from profile_app.database.repositories import ProfileRepository

pwd_context = CryptContext(schemes=['argon2'], deprecated="auto")

def hash_password(user_dict) -> dict:
    """
    Hashing the password from string to argon2 type encryption
    Input: dict = Dictionary of User Details

    """
    user_dict["password"] = pwd_context.hash(user_dict["password"])
    return user_dict

def is_valid_objectId(id) -> HTTPException | Any:
    """
    To check if the string ID is a valid ObjectId string in DB,
    if not valid then throws a HTTPException with status code 400

    Input - id: string

    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId")

def verify_password(hashed_pwd, pwd) -> bool:
    """
    Verify if the password is correct.
    hashed_pwd: Hashed (from the passlib) password in db
    pwd: provided pwd during method call
    """
    return pwd_context.verify(pwd, hashed_pwd)

async def parse_resume(
    file_path: str,
    current_user,
    profile_repo: ProfileRepository
) -> Optional[ProfileResponse]:
    """
    Parse resume file and create profile using repository.
    
    Args:
        file_path: Path to the resume file
        current_user: Current authenticated user
        profile_repo: ProfileRepository instance
        
    Returns:
        ProfileResponse if successful, None otherwise
    """
    profile_json = llm.extract_with_llm(file_path)

    if await profile_repo.exists_by_name(profile_json.get('name', '')):
        print(f"{profile_json.get('name')} already exists")
        return None

    profile_model = ProfileModel(**profile_json)
    profile_model.creator = current_user.email
    pid = await profile_repo.create(profile_model)
    
    if pid:
        profile_data = await profile_repo.find_by_id(pid)
        if profile_data:
            return ProfileResponse(**profile_data)
    
    return None