import typesense

typesenseClient = typesense.Client({
    'nodes': [{
        'host': '2syazxnqwtu1gplop-1.a1.typesense.net',
        'port': '443',
        'protocol': 'https'
    }],
    'api_key': 'EmfeLRfpoQBs0I93JAMq30qj1JuE3i54',  # Replace with your Typesense API key
    'connection_timeout_seconds': 2
})
