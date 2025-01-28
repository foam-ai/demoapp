from fastapi import APIRouter
from app.utils.typesense_client import typesenseClient
from datetime import datetime
from pydantic import BaseModel
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
async def submit_checkout(checkout: CheckoutSubmission):
    checkout["created_at"] = int(datetime.utcnow().timestamp())
    result = typesenseClient.collections['checkout'].documents.create(checkout)
    return {"message": "Checkout request submitted successfully", "data": result}
