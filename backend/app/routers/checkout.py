from fastapi import APIRouter, Response
from app.utils.typesense_client import typesenseClient
from datetime import datetime

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
        return Response(
            status_code=500,
            content={"message": str(e), "success": False},
            media_type="application/json"
        )

