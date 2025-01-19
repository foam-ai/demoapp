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
typesense_port = os.getenv('TYPESENSE_PORT') or "443"
typesense_protocol = os.getenv('TYPESENSE_PROTOCOL') or "https"
typesense_api_key = os.getenv('TYPESENSE_ADMIN_API_KEY') or ""

# Initialize Typesense client
typesenseClient = typesense.Client({
    'nodes': [{
        'host': typesense_host,
        'port': typesense_port,
        'protocol': typesense_protocol
    }],
    'api_key': typesense_api_key,
    'connection_timeout_seconds': 2
})
