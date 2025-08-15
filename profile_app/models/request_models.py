from fastapi import UploadFile, File
from pydantic import Field, EmailStr
from sub_models import *

class LoginRequest(BaseModel):
    """Auth Request Body"""
    username: EmailStr
    password: str

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

class ProfileModel(BaseModel):
    """A complete profile information extracted from the résumé."""
    #Personal Information
    name: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[str] = None

    #Skills
    skills: Skills = Field(default_factory=list)

    #Education
    educations: List[Education] = Field(default_factory=list)

    #Work Experience
    work_experiences: List[WorkExperience] = Field(default_factory=list)

    #Years of Experience
    YoE: Optional[str] =  None
    #Creator(Some User)
    creator_id : str | None = None


class ProfileUpdateRequest(BaseModel):
    name: Optional[str] | None = None
    contact_number: Optional[str] = None
    email: Optional[str] = None
    skills: Skills = Field(default_factory=list)
    educations: List[Education] = Field(default_factory=list)
    work_experiences: List[WorkExperience] = Field(default_factory=list)
    YoE: Optional[str] = None


