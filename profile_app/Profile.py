from datetime import date
from pydantic import BaseModel, Field
from typing import Union, List, Dict, Optional

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
    """A complete profile information extracted from the resume."""
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


