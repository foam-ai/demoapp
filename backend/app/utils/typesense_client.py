import typesense
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file (if you're using one)
load_dotenv()

# Read Typesense configuration from environment variables
typesense_host = os.getenv('TYPESENSE_HOST')
if not typesense_host:
    raise ValueError("TYPESENSE_HOST environment variable is required")

typesense_port = os.getenv('TYPESENSE_PORT') or "443"
typesense_protocol = os.getenv('TYPESENSE_PROTOCOL') or "https"
typesense_api_key = os.getenv('TYPESENSE_ADMIN_API_KEY') or ""

# Initialize Typesense client
typesenseClient = typesense.Client({
    'nodes': [{
    }],
    'api_key': typesense_api_key,
    'connection_timeout_seconds': 2
})

# Verify connection on startup
try:
    typesenseClient.health.retrieve()
    logger.info(f"Successfully connected to Typesense at {typesense_protocol}://{typesense_host}:{typesense_port}")
except Exception as e:
    logger.error(f"Failed to connect to Typesense: {str(e)}")
    raise RuntimeError("Typesense connection failed. Please check your configuration.")
    'api_key': typesense_api_key,
    'connection_timeout_seconds': 2
})
