import typesense
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if you're using one)
load_dotenv()

# Read Typesense configuration from environment variables
typesense_host = os.getenv('TYPESENSE_HOST')
typesense_port = os.getenv('TYPESENSE_PORT')
typesense_protocol = os.getenv('TYPESENSE_PROTOCOL')
typesense_api_key = os.getenv('TYPESENSE_ADMIN_API_KEY')

print("CREDS")
print("HOST", typesense_host)
print("PORT", typesense_port)
print("PROTOCOL", typesense_protocol)
print("API_KEY", typesense_api_key)

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
