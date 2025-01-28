from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.utils.typesense_client import typesenseClient
from datetime import datetime

router = APIRouter()
 
class CheckoutSubmission(BaseModel):
    cardNumber: str
    cvc: str
    zipCode: str
    firstName: str
    lastName: str
    shippingStreet: str
    shippingCity: str
    shippingState: str
    shippingZipCode: str
    shippingMethod: str

@router.post("/checkout")
async def submit_checkout(submission: CheckoutSubmission):
    checkout = {
        "cardNumber": submission.cardNumber,
        "cvc": submission.cvc,
        "zipCode": submission.zipCode,
        "firstName": submission.firstName,
        "lastName": submission.lastName,
        "shippingStreet": submission.shippingStreet,
        "shippingCity": submission.shippingCity,
        "shippingState": submission.shippingState,
        "shippingZipCode": submission.shippingZipCode,
        "shippingMethod": submission.shippingMethod,
        "created_at": int(datetime.utcnow().timestamp())
    }
        
    result = typesenseClient.collections['checkout'].documents.create(checkout)
    return {"message": "Checkout request submitted successfully", "data": result}
