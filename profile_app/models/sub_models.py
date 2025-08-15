from typing import Optional, List

from pydantic import BaseModel


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