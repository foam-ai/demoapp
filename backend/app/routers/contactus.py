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
            "created_at": int(datetime.utcnow().timestamp())
        }
    }
    try:
        logger.info(contact)
        result = typesenseClient.collections['contactus'].documents.create(contact['data'])
        logger.info("Yay it worked.")
        return {"message": "Contact us form submitted successfully", "data": result}
    except Exception as exc:
        contact["status"] = "error"
        contact["error"] = str(exc)
        logger.error(contact)
        logger.error("An error in the contact us endpoint has occurred")
        raise HTTPException(status_code=500, detail=str(exc))