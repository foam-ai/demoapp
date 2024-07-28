from app.routers import quotes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import contactus
import logging
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("myapp")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contactus.router)
app.include_router(quotes.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
