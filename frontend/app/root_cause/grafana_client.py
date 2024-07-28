import os
import asyncio
import aiohttp
from app.metadata import get_user_metadata
from urllib.parse import urlencode

class GrafanaClient:
    def __init__(self, user):
        self.user_id = user['user_id']
        print(user)
        self.grafana_url = user.get('grafana_url', '').strip()
        self.service_account_token = user.get('grafana_service_account_token', '').strip()

        if not self.grafana_url or not self.service_account_token:
            raise ValueError(f"Missing Grafana metadata for user {self.user_id}")

    async def get_dashboard(self, dashboard_uid):
        headers = {
            "Authorization": f"Bearer {self.service_account_token}",
            "Accept": "application/json"
        }
        url = f"{self.grafana_url}/api/dashboards/uid/{dashboard_uid}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.json()

    async def generate_panel_image(self, dashboard_uid, panel_id):
        headers = {
            "Authorization": f"Bearer {self.service_account_token}",
            "Accept": "image/png"
        }
        params = {
            "orgId": "1",
            "panelId": panel_id,
            "width": "1000",
            "height": "500",
            "from": "now-15m",
            "to": "now"
        }
        url = f"{self.grafana_url}/render/d-solo/{dashboard_uid}?{urlencode(params)}"
        async with aiohttp.ClientSession() as session:
            print(url)
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.read()

    async def save_panel_image(self, dashboard_uid, panel_id, output_dir):
        image_data = await self.generate_panel_image(dashboard_uid, panel_id)

        dashboard_details = await self.get_dashboard(dashboard_uid)
        dashboard_name = dashboard_details['dashboard']['title']

        safe_dashboard_name = "".join(c if c.isalnum() else "_" for c in dashboard_name)
        filename = f"{self.user_id}_{safe_dashboard_name}_panel_{panel_id}.png"
        filepath = os.path.join(output_dir, filename)

        os.makedirs(output_dir, exist_ok=True)
        with open(filepath, 'wb') as f:
            f.write(image_data)

        return filepath


async def process_user(user, dashboard_uid, output_dir):
    try:
        grafana_client = GrafanaClient(user)

        dashboard = await grafana_client.get_dashboard(dashboard_uid)

        panel_count = 0
        for panel in dashboard['dashboard']['panels']:
            if 'type' in panel and panel['type'] != 'row':
                image_path = await grafana_client.save_panel_image(dashboard_uid, panel['id'], output_dir)
                print(f"Saved image for user {user['user_id']}, panel {panel['id']} to {image_path}")
                panel_count += 1

        return panel_count
    except ValueError as e:
        print(f"Skipping user {user['user_id']}: {str(e)}")
        return 0
    except Exception as e:
        print(f"An error occurred for user {user['user_id']}: {str(e)}")
        return 0


async def main():
    dashboard_uid = "adr6j9a3p49vke"
    output_dir = "grafana_images"

    user_data = get_user_metadata()

    tasks = [process_user(user, dashboard_uid, output_dir) for user in user_data]
    results = await asyncio.gather(*tasks)

    total_panels = sum(results)
    print(f"Total panels processed: {total_panels}")


if __name__ == "__main__":
    asyncio.run(main())
