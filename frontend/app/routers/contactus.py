from fastapi import APIRouter, HTTPException
from app.models import ContactSubmission
from datetime import datetime
import logging
from app.typesense_client import typesenseClient

router = APIRouter()


@router.post("/contactus")
async def submit_contact(submission: ContactSubmission):
    contact = {
        "name": submission.name,
        "email": submission.email,
        "company": submission.company,
        "title": submission.title,
        "team_size": submission.teamSize,
        "message": submission.message,
        "linkedin": submission.linkedin,
        "created_at": int(datetime.utcnow().timestamp())
    }
    try:
        result = typesenseClient.collections['contact_submissions'].documents.create(contact)
        logging.info("Careers form submitted successfully")
        return {"message": "Contact us form submitted successfully", "data": result}
    except Exception as exc:
        logging.info("Contact us form submission error")
        raise HTTPException(status_code=500, detail=str(exc))
