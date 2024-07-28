import os
from dotenv import load_dotenv
import requests

load_dotenv()

AUTH0_ISSUER_BASE_URL = os.getenv('AUTH0_ISSUER_BASE_URL')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_AUDIENCE = f'{AUTH0_ISSUER_BASE_URL}/api/v2/'


def get_management_api_token():
    """Fetch a new Management API token from Auth0"""
    payload = {
        'client_id': AUTH0_CLIENT_ID,
        'client_secret': AUTH0_CLIENT_SECRET,
        'audience': AUTH0_AUDIENCE,
        'grant_type': 'client_credentials'
    }
    response = requests.post(f'{AUTH0_ISSUER_BASE_URL}/oauth/token', json=payload)
    response.raise_for_status()
    return response.json()['access_token']


def get_all_users():
    """Fetch all users from Auth0"""
    token = get_management_api_token()
    headers = {'Authorization': f'Bearer {token}'}
    url = f'{AUTH0_ISSUER_BASE_URL}/api/v2/users'
    params = {
        'fields': 'user_id,user_metadata',
        'include_fields': 'true',
        'search_engine': 'v3'
    }

    users = []
    while url:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        users.extend(data)
        url = response.links.get('next', {}).get('url')

    return users

def get_user_metadata():
    users = get_all_users()
    user_data = []

    for user in users:
        metadata = user.get('user_metadata', {})
        user_info = {
            'user_id': user['user_id'],
            'github_installation_id': metadata.get('githubInstallationId'),
            'repo_owner': metadata.get('repoOwner'),
            'repo_name': metadata.get('repoName'),
            'grafana_url': metadata.get('grafanaUrl'),
            'grafana_service_account_token': metadata.get('grafanaServiceAccountToken')
        }
        user_data.append(user_info)

    return user_data
