from app.typesense_client import typesenseClient


def get_inventory():
    try:
        result = typesenseClient.collections['robots'].documents.search({
            'q': '*',
            'query_by': '*',
            'per_page': 10,
            'exclude_fields': 'embedding'
        })
        return result['hits']
    except Exception as exc:
        raise Exception(f"Error fetching inventory: {exc}")
