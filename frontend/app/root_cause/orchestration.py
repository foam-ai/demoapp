import asyncio
from datetime import datetime, timedelta
import base64
import os
from app.root_cause.github_client import GitHubClient
from app.root_cause.grafana_client import GrafanaClient
from app.root_cause.chatgpt_client import ChatGPTClient
from app.metadata import get_user_metadata


class AnalysisOrchestrator:
    def __init__(self, user):
        self.user = user
        self.github_client = GitHubClient(user)
        self.grafana_client = GrafanaClient(user)
        self.chatgpt_client = ChatGPTClient()
        self.dashboard_uid = "adr6j9a3p49vke"
        self.grafana_output_dir = "grafana_images"
        self.github_output_dir = "github_diffs"

    async def analyze_dashboard(self):
        dashboard = await self.grafana_client.get_dashboard(self.dashboard_uid)
        issues = []

        for panel in dashboard['dashboard']['panels']:
            if 'type' in panel and panel['type'] != 'row':
                image_path = await self.grafana_client.save_panel_image(self.dashboard_uid, panel['id'],
                                                                        self.grafana_output_dir)
                issue = await self._analyze_panel(image_path, panel)
                if issue:
                    panel_url = f"{self.user['grafana_url']}/d/{self.dashboard_uid}?viewPanel={panel['id']}"
                    issue['panel_url'] = panel_url
                    issue['image_path'] = image_path
                    issue['summary'] = await self.summarize_analysis(issue['issue_description'])
                    issues.append(issue)

        return issues

    async def _analyze_panel(self, image_path, panel):
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        prompt = (f"Analyze this Grafana panel image titled '{panel.get('title', 'Untitled Panel')}'. "
                  f"Identify any issues such as latency increases, HTTP errors (e.g., 500s), or other anomalies. "
                  f"Focus on performance problems and error rates. "
                  f"Please provide the title and any metadata on any problem that may be showing an issue. "
                  f"Describe as much as possible what the panel is showing, the name of the endpoint or the service, what is showing, etc. "
                  f"Describe it as much as possible. Do not provide solutions or anything, focus on solely describing the issue as much as possible. "
                  f"If you cannot find an issue such as a spike, error rates or latency degradation or such things reply with 'SEEMS NORMAL'")

        analysis = self.chatgpt_client.analyze([
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
        ])

        if "SEEMS NORMAL" not in analysis.upper():
            return {
                'panel_id': panel['id'],
                'panel_title': panel.get('title', 'Untitled Panel'),
                'issue_description': analysis
            }
        return None

    async def analyze_prs_for_issue(self, issue):
        since = datetime.utcnow() - timedelta(minutes=30)
        merged_prs = self.github_client.get_merged_pull_requests(since)
        pr_rankings = []

        for pr in merged_prs:
            diff_content = self.github_client.get_pr_diff(pr['number'])
            pr_dir = self.github_client.save_pr_diffs(pr, diff_content)

            with open(os.path.join(pr_dir, 'full_diff.diff'), 'r') as f:
                diff_content = f.read()

            prompt = (
                f"Given this dashboard issue in the panel '{issue['panel_title']}': '{issue['issue_description']}'\n\n"
                f"Analyze this PR diff and determine if it could be the cause of the issue. "
                f"Rate the likelihood on a scale of 1-10, where 10 is most likely.\n\n{diff_content}")

            analysis = self.chatgpt_client.analyze([{"type": "text", "text": prompt}])

            rating = self._extract_rating(analysis)

            pr_rankings.append({
                'pr_number': pr['number'],
                'title': pr['title'],
                'url': pr['html_url'],
                'rating': rating,
                'analysis': analysis
            })

        if pr_rankings:
            most_likely_pr = max(pr_rankings, key=lambda x: x['rating'])
            most_likely_pr['summary'] = await self.summarize_analysis(most_likely_pr['analysis'])
            return most_likely_pr
        return None

    def _extract_rating(self, analysis):
        try:
            return int(analysis.split('Rating:')[1].split('/10')[0].strip())
        except:
            return 0

    async def summarize_analysis(self, full_analysis):
        prompt = (
            "Summarize the following analysis in one concise paragraph. "
            "Focus on the most important points and be as brief as possible:\n\n"
            f"{full_analysis}"
        )
        summary = self.chatgpt_client.analyze([{"type": "text", "text": prompt}])
        return summary


async def main():
    user_data = get_user_metadata()

    for user in user_data:
        orchestrator = AnalysisOrchestrator(user)

        print(f"Analyzing dashboard for user: {user['user_id']}")
        dashboard_issues = await orchestrator.analyze_dashboard()

        if dashboard_issues:
            print(f"Dashboard issues detected: {len(dashboard_issues)}")
            dashboard_url = f"{user['grafana_url']}/d/{orchestrator.dashboard_uid}"
            print(f"Dashboard URL: {dashboard_url}")

            for issue in dashboard_issues:
                print(f"\nIssue in panel '{issue['panel_title']}':")
                print(f"Panel URL: {issue['panel_url']}")
                print(f"Panel image: {issue['image_path']}")
                print(f"Summary: {issue['summary']}")
                print("\nAnalyzing PRs for potential causes...")
                most_likely_pr = await orchestrator.analyze_prs_for_issue(issue)

                if most_likely_pr:
                    print("Most likely PR causing the issue:")
                    print(f"PR #{most_likely_pr['pr_number']}: {most_likely_pr['title']}")
                    print(f"URL: {most_likely_pr['url']}")
                    print(f"Likelihood: {most_likely_pr['rating']}/10")
                    print(f"Summary: {most_likely_pr['summary']}")
                else:
                    print("No PRs found that are likely to cause this issue.")
                print("-" * 60)
        else:
            print("No dashboard issues detected.")

if __name__ == "__main__":
    asyncio.run(main())
