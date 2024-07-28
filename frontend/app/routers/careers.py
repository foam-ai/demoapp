from fastapi import APIRouter, HTTPException
from app.typesense_client import typesenseClient
from app.models import CareersSubmission
from datetime import datetime
import logging

router = APIRouter()


@router.post("/careers")
async def submit_careers(submission: CareersSubmission):
    contact = {
        "name": submission.name,
        "email": submission.email,
        "linkedin": submission.linkedin,
        "created_at": int(datetime.utcnow().timestamp())
    }
    try:
        result = typesenseClient.collections['careers_submissions'].documents.create(contact)
        logging.info("Careers form submitted successfully")
        return {"message": "Careers form submitted successfully", "data": result}
    except Exception as exc:
        logging.info("Careers form submission error")
        raise HTTPException(status_code=500, detail=str(exc))
