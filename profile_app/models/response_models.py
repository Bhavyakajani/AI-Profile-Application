from datetime import datetime

from pydantic import EmailStr, Field
from bson import ObjectId
from sub_models import *

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
    name: str
    email: EmailStr
    role: str

class UserGetResponse(BaseResponseModel):
    name: str
    email: EmailStr | None
    role: str
    stats: Optional[UserStats] = None

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
    name: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    educations: List[Education] = Field(default_factory=list)
    work_experiences: List[WorkExperience] = Field(default_factory=list)
    YoE: Optional[str] = None
    creator: Optional[CreatorResponse]
    created_at: datetime
    updated_at: datetime

class ProfilesListResponse(BaseResponseModel):
    total_count: int
    profiles: List[ProfileResponse]

class ProfileUpdateResponse(BaseResponseModel):
    message: str
    updated_data: ProfileResponse

#--------------Bookmark-----------------
class BookmarkCreateResponse(BaseModel):
    message: str

class BookmarkDeleteResponse(BaseModel):
    message: str


