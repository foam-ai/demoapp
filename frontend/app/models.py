from typing import Optional 
from pydantic import BaseModel


class ContactSubmission(BaseModel):
    name: str
    company: Optional[str] = None
    title: Optional[str] = None
    email: str
    teamSize: Optional[str] = None
    linkedin: Optional[str] = None
    message: Optional[str] = None


class CareersSubmission(BaseModel):
    name: str
    email: str
    linkedin: str
