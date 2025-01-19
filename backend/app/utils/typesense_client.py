import typesense
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Debug: Print environment variables (sanitized)
logger.info("Checking Typesense configuration...")
logger.info(f"TYPESENSE_ADMIN_API_KEY present: {'TYPESENSE_ADMIN_API_KEY' in os.environ}")
logger.info(f"TYPESENSE_PORT present: {'TYPESENSE_PORT' in os.environ}")
logger.info(f"TYPESENSE_PROTOCOL present: {'TYPESENSE_PROTOCOL' in os.environ}")

# Read Typesense configuration
typesense_host = "host"  # This seems hardcoded - make sure this is intentional
typesense_port = os.getenv('TYPESENSE_PORT')
typesense_protocol = os.getenv('TYPESENSE_PROTOCOL')
typesense_api_key = os.getenv('TYPESENSE_ADMIN_API_KEY')

if not typesense_api_key:
    logger.error("TYPESENSE_ADMIN_API_KEY is not set!")
    raise ValueError("TYPESENSE_ADMIN_API_KEY must be set in environment variables")

# Initialize Typesense client
try:
    typesenseClient = typesense.Client({
        'nodes': [{
            'host': typesense_host,
            'port': typesense_port or "443",
            'protocol': typesense_protocol or "https"
        }],
        'api_key': typesense_api_key,
        'connection_timeout_seconds': 2
    })
    logger.info("Typesense client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Typesense client: {e}")
    raise
