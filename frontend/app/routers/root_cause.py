from fastapi import APIRouter, HTTPException
from typing import Dict, List
from app.root_cause.orchestration import AnalysisOrchestrator
from app.metadata import get_user_metadata

router = APIRouter()


@router.post("/root_cause", response_model=Dict)
async def analyze_root_cause():
    try:
        user_data = get_user_metadata()
        all_results = []

        for user in user_data:
            orchestrator = AnalysisOrchestrator(user)
            dashboard_issues = await orchestrator.analyze_dashboard()

            if dashboard_issues:
                dashboard_url = f"{user['grafana_url']}/d/{orchestrator.dashboard_uid}"

                for issue in dashboard_issues:
                    most_likely_pr = await orchestrator.analyze_prs_for_issue(issue)

                    result = {
                        "user_id": user['user_id'],
                        "dashboard_url": dashboard_url,
                        "panel_title": issue['panel_title'],
                        "panel_url": issue['panel_url'],
                        "panel_image": issue['image_path'],
                        "issue_description": issue['issue_description'],
                    }

                    if most_likely_pr and most_likely_pr.get('url'):
                        result.update({
                            "pr_url": most_likely_pr['url'],
                            "pr_title": most_likely_pr['title'],
                            "pr_likelihood": most_likely_pr['rating'],
                            "pr_analysis": most_likely_pr['analysis']
                        })
                        all_results.append(result)

        # Sort results by PR likelihood (descending) and return the top result
        if all_results:
            return sorted(all_results, key=lambda x: x['pr_likelihood'], reverse=True)[0]
        else:
            return {"message": "No issues detected"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test_root_cause")
async def test_root_cause() -> Dict:
    test_response = {
        "user_id": "auth0|6686121fd36b7c562f2d1bd3",
        "dashboard_url": "https://perlagamez.grafana.net/d/adr6j9a3p49vke",
        "panel_title": "HTTP ContactUs Response Status Code",
        "panel_url": "https://perlagamez.grafana.net/d/adr6j9a3p49vke?viewPanel=2",
        "panel_image": "grafana_images/auth0|6686121fd36b7c562f2d1bd3_ContactUs_Client_panel_2.png",
        "issue_description": "The panel titled 'HTTP ContactUs Response Status Code' shows the status of HTTP responses over a given time period. The following observations can be made:\n\n1. The y-axis represents the HTTP status codes (with a value of 200 indicating successful responses).\n2. The x-axis represents the time, ranging from around 04:00 to 04:25.\n\nThere are two significant drops to zero in the graph, occurring at approximately:\n- 04:05\n- 04:15\n\nDuring these times, it appears that there were no 200 status code responses recorded, which may indicate a service outage or failure to process requests successfully for a period of time.\n\n**Issues Observed:**\n1. Two noticeable drops in the graph where the status code responses drop to zero.\n\nOther than these drops, the status code 200 is consistently shown when the service is up, with values ranging between 600 and 700.\n\nThe anomalies in this graph likely indicate periods where the 'ContactUs' endpoint had issues handling requests.\n\n**Summary:**\n- Title: HTTP ContactUs Response Status Code\n- Endpoint/Service: ContactUs\n- Observed Issues: Two significant drops to zero in status code responses at approximately 04:05 and 04:15 indicating potential outages or failures in the service.\n",
        "pr_url": "https://github.com/garage-tech/foam/pull/7",
        "pr_title": "Add nit to backend",
        "pr_likelihood": 0,
        "pr_analysis": "To determine whether the provided Pull Request (PR) diff could be the cause of the observed issues in the \"HTTP ContactUs Response Status Code\" panel, let's analyze the changes:\n\n### Changes Analyzed:\n\n1. **.gitignore changes:**\n   - Trivial change: This simply involves an addition of a newline character at the end of the file, which has no operational effect on the service.\n\n2. **Modifications to contactus.py:**\n\n   \npython\n   # Original\n   try:\n       logging.info(f\"Contact form submitted successfully: {json.dumps(contact)}\")\n       return {\"message\": \"Contact form submitted successfully\", \"data\": contact}\n   except Exception as exc:\n       logging.error(f\"Contact form submission error: {str(exc)}\")\n       raise HTTPException(status_code=500, detail=str(exc))\n\n   # Modified\n   try:\n       # Log the contact submission\n       logging.info(f\"Contact form submitted: {json.dumps(contact)}\")\n       # Simulate an error to always raise an HTTP 500\n       raise Exception(\"Simulated server error\")\n   except Exception as exc:\n       logging.error(f\"Contact form submission error: {str(exc)}\")\n       raise HTTPException(status_code=500, detail=\"Internal Server Error\")\n\n\n   - **Logging message change:** The log message has changed but would still successfully log the same information as before.\n   - **Simulated error:** A deliberate exception is being raised in the new code block. This results in always returning an HTTP 500 status code (\"Internal Server Error\") whenever the submit_contact function is called.\n\n3. **docker-compose.yml changes:**\n   - A trivial change: Addition of a newline character, which has no impact on the service operation itself.\n\n### Analysis:\nThe most critical change in this diff is the simulated server error introduced in the submit_contact function, which forces all submissions to the ContactUs endpoint to result in an HTTP 500 response. This change would directly cause periods where no HTTP 200 responses are recorded, as all attempts to submit to ContactUs would fail with an error.\n\n### Likelihood of the PR being the cause of the issue:\nGiven the modification to always raise an HTTP 500 error, this PR is almost certainly the cause of the observed drops to zero in the HTTP 200 response status. \n\n**Likelihood rating: 10/10**\n\n### Conclusion:\nThe PR diff introduces a simulated server error in the submit_contact function, causing all requests to the ContactUs endpoint to fail. This directly correlates with the observed drops to zero in the panel for the HTTP 200 status code and is highly likely to be the root cause of the issue noted in the dashboard."
    }

    return test_response

