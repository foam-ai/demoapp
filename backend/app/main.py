from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import checkout_router
from dotenv import load_dotenv
from sentry_sdk.integrations.fastapi import FastApiIntegration

import sentry_sdk


sentry_sdk.init(
    dsn="https://3b253535b6f12e1507b24d706c738b87@o4508066025832448.ingest.us.sentry.io/4508671357222912",
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
app.include_router(checkout_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0
