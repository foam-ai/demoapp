from fastapi import APIRouter, HTTPException
# from app.utils.typesense_client import typesenseClient
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
    endpoint_start_time = time.time()
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
        # result = typesenseClient.collections['quotes'].documents.create(quote['data'])
        result = "blah"
        endpoint_end_time = time.time()
        total_latency = (endpoint_end_time - endpoint_start_time) * 1000  # Convert to milliseconds
        quote["total_endpoint_latency"] = f"{total_latency:.2f}ms"

        logger.info(quote)
        return {"message": "Quote request submitted successfully", "data": result}
    except ValueError as ve:
        quote["status"] = "error"
        quote["error"] = f"Configuration error: {str(ve)}"
        logger.error(quote)
        raise HTTPException(status_code=500, detail=str(ve))
    except requests.RequestException as req_exc:
        quote["status"] = "error"
        quote["error"] = f"Ownership endpoint error: {str(req_exc)}"
        logger.error(quote)
        raise HTTPException(status_code=500, detail=str(req_exc))
    except Exception as exc:
        quote["status"] = "error"
        quote["error"] = str(exc)
        logger.error(quote)
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        if "total_endpoint_latency" not in quote:
            endpoint_end_time = time.time()
            total_latency = (endpoint_end_time - endpoint_start_time) * 1000
            quote["total_endpoint_latency"] = f"{total_latency:.2f}ms"
        logger.info(quote)
