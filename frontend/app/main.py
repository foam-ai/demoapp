from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import contactus, careers, github_webhook, root_cause
import logging
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

logging.basicConfig(level=logging.INFO)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(contactus.router)
app.include_router(careers.router)
app.include_router(github_webhook.router)
app.include_router(root_cause.router)
