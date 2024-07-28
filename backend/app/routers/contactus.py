from fastapi import APIRouter, HTTPException
from app.utils.models import ContactSubmission
from datetime import datetime
import logging
from app.utils.typesense_client import typesenseClient

router = APIRouter()
logger = logging.getLogger("myapp")


@router.post("/contactus")
async def submit_contact(submission: ContactSubmission):
    contact = {
        "name": submission.name,
        "email": submission.email,
        "phone_number": submission.phone_number,
        "message": submission.message,
        "created_at": int(datetime.utcnow().timestamp())
    }
    try:
        result = typesenseClient.collections['contactus'].documents.create(contact)
        logger.info("Contact form submitted successfully")
        return {"message": "Contact us form submitted successfully", "data": result}
    except Exception as exc:
        logging.error(f"Contact us form submission error: {str(exc)}")
        raise HTTPException(status_code=500, detail=str(exc))
