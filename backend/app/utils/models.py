from typing import Optional 
from pydantic import BaseModel


class ContactSubmission(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    message: Optional[str] = None


class QuoteSubmission(BaseModel):
    product_name: Optional[str] = None
    condition: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    name: Optional[str] = None
    company_name: Optional[str] = None
    message: Optional[str] = None
    zipcode: Optional[str] = None