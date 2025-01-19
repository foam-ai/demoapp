from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.utils.typesense_client import typesenseClient
from datetime import datetime

router = APIRouter()

class CheckoutSubmission(BaseModel):
    card_number: Optional[str] = None
    zipcode: Optional[str] = None

@router.post("/checkout")
async def submit_checkout(submission: CheckoutSubmission):
    checkout = {
            "card_number": submission.card_number,
            "zipcode": submission.zipcode,
            "created_at": int(datetime.utcnow().timestamp())
        }
    result = typesenseClient.collections['checkout'].documents.create(checkout)
    return {"message": "Checkout request submitted successfully", "data": result}
