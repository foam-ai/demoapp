from fastapi import APIRouter
from app.utils.typesense_client import typesenseClient
from app.utils.models import QuoteSubmission
from datetime import datetime

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
    result = typesenseClient.collections['quotes'].documents.create(quote['data'])
    return {"message": "Quote request submitted successfully", "data": result}
