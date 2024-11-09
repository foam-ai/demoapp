from app.routers import quotes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import contactus
from dotenv import load_dotenv

import sentry_sdk

sentry_sdk.init(
    dsn="https://61eb4dffc8c8cca0357b1653e6bf4074@o4508066025832448.ingest.us.sentry.io/4508270836121600",
)

load_dotenv()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contactus.router)
app.include_router(quotes.router)


@app.head("/")
def read_root():
    return {"Hello": "World"}


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/divide/{divisor}")
def divide(divisor: int):
    result = 1 / divisor
    return {"result": result}
