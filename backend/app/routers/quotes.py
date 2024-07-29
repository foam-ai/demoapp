from fastapi import APIRouter, HTTPException
from app.utils.typesense_client import typesenseClient
from app.utils.models import QuoteSubmission
from datetime import datetime
from app.utils.logger import logger

router = APIRouter()


@router.post("/quotes")
async def submit_quote(submission: QuoteSubmission):
    endpoint = "/quotes"
    quote = {
        "endpoint": endpoint,
        "status": "success",
        "data": {
            "product_name": submission.product_name,
            "condition": submission.condition,
            "email": submission.email,
            "phone_number": submission.phone_number,
            "name": submission.name,
            "company_name": submission.company_name,
            "message": submission.message,
            "zipcode": submission.zipcode,
            "created_at": int(datetime.utcnow().timestamp())
        }
    }
    try:
        result = typesenseClient.collections['quotes'].documents.create(quote['data'])
        logger.info(quote)
        return {"message": "Quote request submitted successfully", "data": result}
    except Exception as exc:
        quote["status"] = "error"
        quote["error"] = str(exc)
        logger.error(quote)
        raise HTTPException(status_code=500, detail=str(exc))
