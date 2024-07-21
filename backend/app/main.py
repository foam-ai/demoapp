from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.typesense_client import typesenseClient
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from datetime import datetime
import boto3
import os
import json
from dotenv import load_dotenv
from app.utils import call_open_ai

load_dotenv()

app = FastAPI()

# AWS S3 setup
s3_client = boto3.client('s3',
                         aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                         aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                         region_name=os.getenv('AWS_REGION'))
bucket_name = os.getenv('AWS_BUCKET_NAME')


class Item(BaseModel):
    name: str
    description: str


class RequestForProduct(BaseModel):
    user_id: str
    description: Optional[str] = None
    images: List[str] = []


class ContactSubmission(BaseModel):
    name: str
    email: str
    phone_number: str
    message: str


class QuoteRequest(BaseModel):
    product_name: str
    condition: str
    email: str
    phone_number: str
    name: str
    company_name: str
    message: str
    zipcode: str


class OpenAIRequest(BaseModel):
    prompt: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/create_quote")
async def create_quote(quote_request: QuoteRequest):
    try:
        document = quote_request.dict()
        document['created_at'] = int(datetime.utcnow().timestamp())

        result = typesenseClient.collections['quote_requests'].documents.create(document)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/submit_contact")
async def submit_contact(submission: ContactSubmission):
    contact = {
        "name": submission.name,
        "email": submission.email,
        "phone_number": submission.phone_number,
        "message": submission.message,
        "created_at": int(datetime.utcnow().timestamp())
    }
    
    try:
        result = typesenseClient.collections['contact'].documents.create(contact)
        return {"message": "Contact information submitted successfully", "data": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/openai")
async def openai_endpoint(request: OpenAIRequest):
    try:
        product_name = request.prompt.strip().lower()
        if product_name:
            result = call_open_ai(product_name)
            return {"content": json.loads(result.replace("json\n", "").replace("`", ""))}
        else: 
            return {"content": {}}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
