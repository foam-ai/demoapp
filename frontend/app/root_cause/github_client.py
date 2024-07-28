import os
import time
import requests
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
from app.metadata import get_user_metadata

load_dotenv()

# GitHub configuration
GITHUB_APP_ID = int(os.getenv('GITHUB_APP_ID'))
PRIVATE_KEY = os.getenv("GITHUB_PRIVATE_KEY").replace("\\n", "\n")
OUTPUT_DIR = 'github_diffs'  # Base directory for storing diffs


class GitHubClient:
    def __init__(self, user):
        self.user_id = user['user_id']
        self.installation_id = user.get('github_installation_id')
        self.repo_owner = user.get('repo_owner')
        self.repo_name = user.get('repo_name')

        if not self.installation_id or not self.repo_owner or not self.repo_name:
            raise ValueError(f"Missing GitHub metadata for user {self.user_id}")

        self.repo = f"{self.repo_owner}/{self.repo_name}"
        self.access_token = self._get_access_token()

    def _get_jwt(self):

        payload = {
            'iat': int(time.time()),
            'exp': int(time.time()) + (10 * 60),
            'iss': GITHUB_APP_ID
        }

        return jwt.encode(payload, PRIVATE_KEY, algorithm='RS256')

    def _get_access_token(self):
        jwt_token = self._get_jwt()
        url = f'https://api.github.com/app/installations/{self.installation_id}/access_tokens'
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()['token']

    def get_merged_pull_requests(self, since):
        url = f'https://api.github.com/repos/{self.repo}/pulls'
        headers = {
            'Authorization': f'token {self.access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        params = {
            'state': 'closed',
            'base': 'main',
            'sort': 'updated',
            'direction': 'desc',
            'per_page': 100
        }

        merged_prs = []
        while url:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            pull_requests = response.json()

            for pr in pull_requests:
                if pr.get('merged_at'):
                    merged_at = datetime.strptime(pr['merged_at'], '%Y-%m-%dT%H:%M:%SZ')
                    if merged_at >= since:
                        merged_prs.append(pr)
                    else:
                        return merged_prs

            url = response.links.get('next', {}).get('url')
            params = {}  # Clear params for subsequent requests

        return merged_prs

    def get_pr_diff(self, pr_number):
        url = f'https://api.github.com/repos/{self.repo}/pulls/{pr_number}'
        headers = {
            'Authorization': f'token {self.access_token}',
            'Accept': 'application/vnd.github.v3.diff'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text

    def save_pr_diffs(self, pr, diff_content):
        # Create a safe directory name from the PR title
        safe_pr_name = "".join(c if c.isalnum() or c in [' ', '-', '_'] else '_' for c in pr['title'])
        safe_pr_name = f"PR_{pr['number']}_{safe_pr_name[:50]}"  # Limit length and add PR number

        # Create directory for this PR
        pr_dir = os.path.join(OUTPUT_DIR, self.user_id, safe_pr_name)
        os.makedirs(pr_dir, exist_ok=True)

        # Save the full diff
        full_diff_path = os.path.join(pr_dir, 'full_diff.diff')
        with open(full_diff_path, 'w', encoding='utf-8') as f:
            f.write(diff_content)

        # Parse the diff to separate files
        files = diff_content.split('diff --git ')
        for file_diff in files[1:]:  # Skip the first empty element
            file_lines = file_diff.split('\n')
            file_name = file_lines[0].split(' b/')[-1]
            safe_file_name = "".join(c if c.isalnum() or c in ['.', '-', '_'] else '_' for c in file_name)
            file_path = os.path.join(pr_dir, safe_file_name + '.diff')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('diff --git ' + file_diff)

        return pr_dir


def main():
    user_data = get_user_metadata()

    for user in user_data:
        try:
            github_client = GitHubClient(user)

            since = datetime.utcnow() - timedelta(minutes=30)
            merged_prs = github_client.get_merged_pull_requests(since)

            print(f"User: {user['user_id']}")
            print(f"Merged pull requests in the last 10 minutes:")
            for pr in merged_prs:
                print(f"PR #{pr['number']}: {pr['title']}")
                print(f"Merged at: {pr['merged_at']}")
                print(f"URL: {pr['html_url']}")

                # Get and save diff
                diff_content = github_client.get_pr_diff(pr['number'])
                pr_dir = github_client.save_pr_diffs(pr, diff_content)
                print(f"Diff files saved in: {pr_dir}")
                print('-' * 60)

        except ValueError as e:
            print(f"Skipping user {user['user_id']}: {str(e)}")
        except Exception as e:
            print(f"An error occurred for user {user['user_id']}: {str(e)}")


if __name__ == '__main__':
    main()