from app.routers import quotes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import contactus
from dotenv import load_dotenv

import sentry_sdk

sentry_sdk.init(
    dsn="https://7fc43ecd41b8e1b761484815ccc617c5@o4508066025832448.ingest.us.sentry.io/4508632977637376",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    _experiments={
        # Set continuous_profiling_auto_start to True
        # to automatically start the profiler on when
        # possible.
        "continuous_profiling_auto_start": True,
    },
)
load_dotenv()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.digitaldemoapp.com/"],
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

@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0