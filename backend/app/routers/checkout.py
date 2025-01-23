from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.utils.typesense_client import typesenseClient
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

class CheckoutSubmission(BaseModel):
    cardnumber: Optional[str] = None
    zipcode: Optional[str] = None

@router.post("/checkout")
async def submit_checkout(submission: CheckoutSubmission):
    try:
        checkout = {
            "cardnumber": submission.cardnumber,
            "zipcode": submission.zipcode,
            "created_at": int(datetime.utcnow().timestamp())
        }
        result = typesenseClient.collections['checkout'].documents.create(checkout)
        logger.info(f"Successfully processed checkout for zipcode: {submission.zipcode}")
        return {"message": "Checkout request submitted successfully", "data": result}
    except Exception as e:
        logger.error(f"Checkout failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process checkout. Please try again later."
        )
