from fastapi import APIRouter, status
from app.utils.typesense_client import typesenseClient
from datetime import datetime
from typing import Dict
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/checkout")
async def submit_checkout(checkout: Dict):
    try:
        checkout["created_at"] = int(datetime.utcnow().timestamp())
        result = typesenseClient.collections['checkout'].documents.create(checkout)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Checkout request submitted successfully",
                "data": result
            }
        )

    except Exception as e:
        return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": str(e.message)}
            )
