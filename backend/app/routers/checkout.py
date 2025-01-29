from fastapi import APIRouter, Response
from app.utils.typesense_client import typesenseClient
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/checkout")
async def submit_checkout(checkout: dict):
    try:
        checkout["created_at"] = int(datetime.utcnow().timestamp())
        result = typesenseClient.collections['checkout'].documents.create(checkout)
        return {
            "message": "Checkout request submitted successfully", 
            "data": result,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error submitting checkout: {e}")
        return {
            "message": str(e),
            "data": None,
            "success": False
        }
