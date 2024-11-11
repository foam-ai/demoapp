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
typesense_host = 'host'
typesense_port = os.getenv('TYPESENSE_PORT')
typesense_protocol = os.getenv('TYPESENSE_PROTOCOL')
typesense_api_key = os.getenv('TYPESENSE_ADMIN_API_KEY')

logger.debug(f"TYPESENSE_HOST: {typesense_host}")
logger.debug(f"TYPESENSE_PORT: {typesense_port}")
logger.debug(f"TYPESENSE_PROTOCOL: {typesense_protocol}")
logger.debug(f"TYPESENSE_ADMIN_API_KEY: {'*' * len(typesense_api_key) if typesense_api_key else 'Not set'}")


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
