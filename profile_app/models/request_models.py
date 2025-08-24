from fastapi import UploadFile, File
from pydantic import Field, EmailStr
from .sub_models import *

class LoginRequest(BaseModel):
    """Auth Request Body"""
    username: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

class UserCreateRequest(BaseModel):
    """Request Body for creating a new user"""
    name: str
    email: EmailStr
    password: str
    role: str  # "admin" or "member"

class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None

class ProfileCreateRequest(BaseModel):
    """file: UploadFile = File(...) multipart form"""
    file: UploadFile = File(...)

class Creator(BaseModel):
    name: str
    email: str

class ProfileModel(BaseModel):
    """A complete profile information extracted from the résumé."""
    #Personal Information
    name: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[str] = None

    #Skills
    skills: List[str] = Field(default_factory=list)

    #Education
    educations: List[Education] = Field(default_factory=list)

    #Work Experience
    work_experiences: List[WorkExperience] = Field(default_factory=list)

    #Years of Experience
    YoE: Optional[str] =  None
    #Creator(Some User)
    creator : str | None = None


class User(BaseModel):
    name: str
    email: str
    password: str
    profiles: Optional[List[ProfileModel]] = []

class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[str] = None
    skills:  Optional[Skills] = None
    educations: Optional[List[Education]] = None
    work_experiences: Optional[List[WorkExperience]] = None
    YoE: Optional[str] = None

#---------------- Bookmark ------------------
class BookmarkCreateRequest(BaseModel):
    profile_id: str

class BookmarkDeleteRequest(BaseModel):
    profile_id: str

