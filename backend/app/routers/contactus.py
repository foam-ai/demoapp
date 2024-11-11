from fastapi import APIRouter
from app.utils.models import ContactSubmission
from datetime import datetime
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
            "created_at": datetime.utcnow().timestamp()
        }
    }
    result = typesenseClient.collections['contactus'].documents.create(contact['data'])
    return {"message": "Contact us form submitted successfully", "data": result}
