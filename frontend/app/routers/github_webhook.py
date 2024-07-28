from fastapi import APIRouter, HTTPException, Request
from datetime import datetime, timedelta
import hmac
import hashlib
import os
import logging
import requests
import base64
import jwt
import difflib
from app.metadata import get_user_metadata

router = APIRouter()

GITHUB_SECRET = os.getenv("GITHUB_SECRET")
GITHUB_APP_ID = os.getenv("GITHUB_APP_ID")
PRIVATE_KEY = os.getenv("GITHUB_PRIVATE_KEY").replace("\\n", "\n")
WEBHOOK_LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'webhook_payload.txt')

# Ensure directories exist
# os.makedirs(os.path.join(os.path.dirname(__file__), 'diffs'), exist_ok=True)


def verify_signature(secret, signature, data):
    if not signature:
        logging.error("No signature provided.")
        return False
    try:
        sha_name, signature = signature.split('=', 1)
        if sha_name != 'sha256':
            logging.error(f"Unexpected sha_name: {sha_name}")
            return False

        mac = hmac.new(secret.encode(), msg=data, digestmod=hashlib.sha256)
        if not hmac.compare_digest(mac.hexdigest(), signature):
            logging.error(f"Signature mismatch: calculated {mac.hexdigest()} != received {signature}")
            return False
        return True
    except Exception as e:
        logging.error(f"Error verifying signature: {str(e)}")
        return False


def generate_jwt(app_id):
    payload = {
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=10),
        'iss': app_id
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm='RS256')


def get_installation_access_token(app_id, installation_id):
    jwt_token = generate_jwt(app_id)
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.post(
        f'https://api.github.com/app/installations/{installation_id}/access_tokens',
        headers=headers
    )
    response.raise_for_status()
    return response.json()['token']


def fetch_pr_changes(repo_full_name, pr_number, access_token):
    url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}/files"
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def fetch_file_content(repo_full_name, path, ref, access_token):
    url = f"https://api.github.com/repos/{repo_full_name}/contents/{path}?ref={ref}"
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        logging.warning(f"File not found: {path} at ref {ref}")
        return None
    response.raise_for_status()
    file_content = response.json()
    if file_content.get("encoding") == "base64":
        return base64.b64decode(file_content.get("content")).decode('utf-8')
    return file_content.get("content")


def save_diff_file(file_path, old_content, new_content):
    if old_content is not None and new_content is not None:
        diff = difflib.unified_diff(
            old_content.splitlines(), new_content.splitlines(),
            fromfile='old', tofile='new', lineterm=''
        )
        diff_content = '\n'.join(diff)
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as file:
                file.write(diff_content)
            logging.info(f"Diff file saved: {file_path}")
        except Exception as e:
            logging.error(f"Error saving diff file {file_path}: {str(e)}")


@router.post("/webhook")
async def handle_webhook(request: Request):
    try:
        payload = await request.body()
        signature = request.headers.get('X-Hub-Signature-256')
        event = request.headers.get('X-GitHub-Event')

        # Write the raw payload and headers to a local text file
        with open(WEBHOOK_LOG_FILE_PATH, 'a') as log_file:
            log_file.write(f"Timestamp: {datetime.now().isoformat()}\n")
            log_file.write(f"Event: {event}\n")
            log_file.write("Headers:\n")
            for header, value in request.headers.items():
                log_file.write(f"{header}: {value}\n")
            log_file.write("\nRaw Payload:\n")
            log_file.write(payload.decode())
            log_file.write("\n\n")

        if not verify_signature(GITHUB_SECRET, signature, payload):
            logging.warning(
                f"GitHub signature verification failed. Signature: {signature}, Payload: {payload.decode()}")
            raise HTTPException(status_code=400, detail="Invalid signature")

        data = await request.json()
        action = data.get("action")
        pull_request = data.get("pull_request", {})
        pr_number = pull_request.get("number")
        pr_title = pull_request.get("title")
        pr_url = pull_request.get("html_url")
        merged = pull_request.get("merged", False)
        base_branch = pull_request.get("base", {}).get("ref")
        repo_full_name = pull_request.get("base", {}).get("repo", {}).get("full_name")
        base_sha = pull_request.get("base", {}).get("sha")
        head_sha = pull_request.get("head", {}).get("sha")

        logging.info(f"GitHub event: {event}, Action: {action}, PR #{pr_number} - {pr_title}")

        if event == "pull_request":
            if action == "closed" and merged and base_branch == "main":
                logging.info(f"Pull request merged: {pr_title} ({pr_url})")
            elif action == "opened":
                logging.info(f"Pull request created: {pr_title} ({pr_url})")
            elif action == "closed":
                logging.info(f"Pull request closed: {pr_title} ({pr_url})")
            else:
                logging.info(f"Pull request {action}: {pr_title} ({pr_url})")

            user_data = get_user_metadata()
            for user in user_data:
                if user['repo_owner'] in repo_full_name and user['repo_name'] in repo_full_name:
                    installation_id = user['github_installation_id']
                    break
            else:
                raise HTTPException(status_code=404, detail="Installation ID not found for the repository")

            # Get installation access token
            access_token = get_installation_access_token(GITHUB_APP_ID, installation_id)

            # Fetch code changes
            changes = fetch_pr_changes(repo_full_name, pr_number, access_token)
            for change in changes:
                filename = change.get("filename")
                logging.info(f"File changed: {filename}")

                # Fetch old and new file content
                old_content = fetch_file_content(repo_full_name, filename, base_sha, access_token)
                new_content = fetch_file_content(repo_full_name, filename, head_sha, access_token)

                # Save diff file
                diff_file_path = os.path.join(os.path.dirname(__file__), 'diffs', f"{filename}.diff")
                save_diff_file(diff_file_path, old_content, new_content)
                logging.info(f"Diff of {filename} saved to {diff_file_path}")

        return {"message": "Webhook received"}
    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Main function for local testing
def main():
    logging.basicConfig(level=logging.INFO)

    # Test reading private key
    logging.info(f"Private key read successfully: {PRIVATE_KEY[:30]}...")  # Print only the first 30 characters

    # Test writing a diff file
    old_test_content = "This is the old test content for writing to a file."
    new_test_content = "This is the new test content for writing to a file."
    diff_test_file_path = os.path.join(os.path.dirname(__file__), 'diffs', 'test_file.diff')
    try:
        save_diff_file(diff_test_file_path, old_test_content, new_test_content)
        logging.info(f"Test diff file written successfully to {diff_test_file_path}")
    except Exception as e:
        logging.error(f"Failed to write test diff file: {str(e)}")


if __name__ == "__main__":
    main()
