from datetime import date

from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict
from typing import Union, List, Dict, Optional

from profile_app.object_id import PyObjectId


class Education(BaseModel):
    degree: Optional[str] = None
    institution: str = None
    start_date: Optional[str] = None # Format: "YYYY-MM" or "YYYY"
    end_date: Optional[str] = None   # Format: "YYYY-MM" or "YYYY"
    location: Optional[str] = None
    cgpa: Optional[str] = None

class WorkExperience(BaseModel):
    company: Optional[str] = None
    start_date: Optional[str] = None # Format: "YYYY-MM" or "YYYY"
    end_date: Optional[str] = None   # Format: "YYYY-MM" or "YYYY"
    location: Optional[str] = None
    role: Optional[str] = None
    currently_working: Optional[bool] = False

class Skills(BaseModel):
    skills: List[str]

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
    creator_id : Optional[str] = None



class ProfilesCollection(BaseModel):
    """List of all the Profiles"""
    profiles: List[ProfileModel]

class User(BaseModel):
    name: str
    email: str
    password: str
    profiles: Optional[List[ProfileModel]] = []

class Creator(BaseModel):
    name: str
    email: str

class ShowProfile(ProfileModel):
    """Response Model for Profiles"""
    # id: PyObjectId = Field(alias="_id")  # This maps Mongo’s `_id` to `id` in response
    creator: Optional[Creator]
    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
        }

class ShowUser(BaseModel):
    """Response Model for User"""
    name: str
    email: str
    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
        }

class UpdateUserResponse(BaseModel):
    message: str
    updated_data: dict

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None









