from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import checkout
from dotenv import load_dotenv
from sentry_sdk.integrations.fastapi import FastApiIntegration

import sentry_sdk


sentry_sdk.init(
    dsn="https://9a01a9376a3e4e62249f887870298bf2@o4508066025832448.ingest.us.sentry.io/4508637820747776",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    integrations=[
        FastApiIntegration(),  # Add this line
    ],
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    