from fastapi import APIRouter, HTTPException
from app.utils.models import ContactSubmission
from datetime import datetime
from app.utils.logger import logger
from app.utils.typesense_client import typesenseClient

router = APIRouter()


@router.post("/contactus")
async def submit_contact(submission: ContactSubmission):
    endpoint = "/contactus"
    contact = {
        "endpoint": endpoint,
        "status": "success",
        "data": {
            "name": submission.name,
            "email": submission.email,
            "phone_number": submission.phone_number,
            "message": submission.message,
        }
    }
    try:
        logger.info("This is a log message from contact us endpoint")
        result = typesenseClient.collections['contactus'].documents.create(contact['data'])
        logger.info(contact)
        return {"message": "Contact us form submitted successfully", "data": result}
    except Exception as exc:
        contact["status"] = "error"
        contact["error"] = str(exc)
        logger.error(contact)
        logger.error("This is an error message from contact us endpoint")
        raise HTTPException(status_code=500, detail=str(exc))
