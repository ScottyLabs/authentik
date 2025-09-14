import requests
import os
from dotenv import load_dotenv
from utils import Utils

load_dotenv()


class AuthentikGroupManager:
    def __init__(self):
        self.token = os.getenv("AUTHENTIK_API_TOKEN")
        self.url = os.getenv("AUTHENTIK_API_URL")

    def create_authentik_group(self, group_name) -> str | None:
        create_group_url = f"{self.url}/api/v3/core/groups/"
        response = requests.post(
            create_group_url,
            json={"name": group_name},
            headers={"Authorization": f"Bearer {self.token}"},
        )
        Utils.print_response(response)
        if not response.ok:
            return None

        return response.json()["pk"]
