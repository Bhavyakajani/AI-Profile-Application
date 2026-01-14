from datetime import datetime
from pydantic import EmailStr, Field, BaseModel
from bson import ObjectId

from .request_models import ProfileModel
from .sub_models import Education, WorkExperience
from typing import List, Optional

class BaseResponseModel(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

#--------Authentication--------
class LoginResponse(BaseModel):
    access_token: str
    token_type: str

#--------------User-----------------

class UserStats(BaseResponseModel):
    total_created_profiles: int = 0
    total_bookmarked_profiles: int = 0

class UserCreateResponse(BaseResponseModel):
    id: str
    name: str
    email: EmailStr
    role: Optional[str] = None
    status: str
    profiles: Optional[List[ProfileModel]] = []

class UserRoleResponse(BaseResponseModel):
    id: str
    name: str
    email: EmailStr
    role: Optional[str]
    status: str

class UserGetResponse(BaseResponseModel):
    id: str
    name: str
    email: EmailStr | None
    role: str

class UserUpdateResponse(BaseResponseModel):
    message: str
    updated_data: UserGetResponse

#--------------Creator-----------------
class CreatorResponse(BaseResponseModel):
    name: str
    email: str

#--------------Profile-----------------
class ProfileResponse(BaseResponseModel):
    """POST and GET Profile Response"""
    id: str = Field(alias='_id', serialization_alias='id', default=None)
    name: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    educations: List[Education] = Field(default_factory=list)
    work_experiences: List[WorkExperience] = Field(default_factory=list)
    YoE: Optional[str] = None
    creator: str | None = None

class ProfilesListResponse(BaseResponseModel):
    total_count: int | None
    profiles: List[ProfileResponse]

class ProfileUpdateResponse(BaseResponseModel):
    message: str
    updated_data: ProfileResponse

#--------------Bookmark-----------------
class BookmarkCreateResponse(BaseModel):
    message: str

class BookmarkDeleteResponse(BaseModel):
    message: str

#---------------File------------------
class FileMetadata(BaseResponseModel):
    file_id: str
    original_name: str
    stored_name: str
    content_type: str
    size: int
    uploaded_at: datetime

class FileUploadResponse(BaseResponseModel):
    """Response model for file upload + parsing"""
    message: str
    metadata: FileMetadata