from app.routers import quotes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import contactus
from dotenv import load_dotenv
import sentry_sdk

sentry_sdk.init(
    dsn="https://594b34c48406e282fbb1a64e5896a266@o4508066025832448.ingest.us.sentry.io/4508122737278976",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
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
