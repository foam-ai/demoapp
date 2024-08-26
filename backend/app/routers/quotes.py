from fastapi import APIRouter, HTTPException
from app.utils.typesense_client import typesenseClient
from app.utils.models import QuoteSubmission
from app.utils.logger import logger
from datetime import datetime
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

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
        if not third_party_client_host_url:
            raise ValueError("THIRD_PARTY_CLIENT_HOST_URL is not set in the environment variables")

        check_ownership_url = f"{third_party_client_host_url}/check_phone_number_ownership"
        ownership_check_data = {
            "name": submission.name,
            "phone_number": submission.phone_number
        }

        start_time = time.time()
        try:
            ownership_response = requests.post(check_ownership_url, json=ownership_check_data, timeout=10)
            ownership_response.raise_for_status()
        finally:
            end_time = time.time()
            latency = (end_time - start_time) * 1000  # Convert to milliseconds
            logger.info({
                "metric": "ownership_endpoint_latency",
                "value": latency,
                "unit": "ms",
                "status": ownership_response.status_code
            })

        result = typesenseClient.collections['quotes'].documents.create(quote['data'])
        logger.info(quote)
        logger.info("Quote submission successful")
        return {"message": "Quote request submitted successfully", "data": result}
    except ValueError as ve:
        quote["status"] = "error"
        quote["error"] = f"Configuration error: {str(ve)}"
        logger.error(quote)
        logger.error("Configuration error in the quotes endpoint")
        raise HTTPException(status_code=500, detail=str(ve))
    except requests.RequestException as req_exc:
        quote["status"] = "error"
        quote["error"] = f"Ownership endpoint error: {str(req_exc)}"
        logger.error(quote)
        logger.error("Ownership endpoint error in the quotes endpoint")
        raise HTTPException(status_code=500, detail=str(req_exc))
    except Exception as exc:
        quote["status"] = "error"
        quote["error"] = str(exc)
        logger.error(quote)
        logger.error("An error in the quotes endpoint has occurred")
        raise HTTPException(status_code=500, detail=str(exc))
