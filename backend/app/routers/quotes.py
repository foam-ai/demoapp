from fastapi import APIRouter, HTTPException
from app.utils.typesense_client import typesenseClient
from app.utils.models import QuoteSubmission
from datetime import datetime
from app.utils.logger import logger
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the third-party client host URL from environment variables
third_party_client_host_url = os.getenv('THIRD_PARTY_CLIENT_HOST_URL')

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

        # Call the check_phone_number_ownership endpoint using the URL from environment variables
        if not third_party_client_host_url:
            raise ValueError("THIRD_PARTY_CLIENT_HOST_URL is not set in the environment variables")

        check_ownership_url = f"{third_party_client_host_url}/check_phone_number_ownership"
        ownership_check_data = {
            "name": submission.name,
            "phone_number": submission.phone_number
        }
        ownership_response = requests.post(check_ownership_url, json=ownership_check_data, timeout=10)
        ownership_response.raise_for_status()

        logger.info(quote)
        logger.info(f"Phone ownership check response: {ownership_response.json()}")
        return {
            "message": "Quote request submitted successfully",
            "data": result,
            "phone_ownership_check": ownership_response.json()
        }
    except ValueError as ve:
        logger.error(f"Configuration error: {str(ve)}")
        raise HTTPException(status_code=500, detail=str(ve))
    except requests.RequestException as req_exc:
        quote["status"] = "error"
        quote["error"] = f"Phone ownership check error: {str(req_exc)}"
        logger.error(quote)
        raise HTTPException(status_code=500, detail=str(req_exc))
    except Exception as exc:
        quote["status"] = "error"
        quote["error"] = str(exc)
        logger.error(quote)
        raise HTTPException(status_code=500, detail=str(exc))
