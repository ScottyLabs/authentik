import requests
import os
from dotenv import load_dotenv
from utils import Utils

load_dotenv()


class HashicorpManager:
    def __init__(self, project_name):
        self.project_name = project_name
        self.token = os.getenv("HASHICORP_API_TOKEN")
        self.api_url = os.getenv("HASHICORP_API_URL")
        self.admin_policy = """\
path "/ScottyLabs/data/{project_name}/*" {{
    capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}}

path "/ScottyLabs/metadata/{project_name}/*" {{
    capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}}\
""".format(project_name=project_name)

        self.developer_policy = """\
path "/ScottyLabs/data/{project_name}/*" {{
    capabilities = ["read", "list"]
}}
""".format(project_name=project_name)

    def create_admin_policy(self, project_name):
        print(f"Creating admin policy for {project_name}")
        response = requests.post(
            f"{self.api_url}/v1/sys/policy/{project_name}-{Utils.ADMIN_SUFFIX}",
            json={"policy": self.admin_policy},
            headers={"X-Vault-Token": self.token},
        )
        Utils.print_response(response)

    def create_developer_policy(self, project_name):
        print(f"Creating developer policy for {project_name}")
        response = requests.post(
            f"{self.api_url}/v1/sys/policy/{project_name}-{Utils.DEVELOPER_SUFFIX}",
            json={"policy": self.developer_policy},
            headers={"X-Vault-Token": self.token},
        )
        Utils.print_response(response)

    def create_admin_group(self, project_name):
        return self.create_group(project_name, Utils.ADMIN_SUFFIX)

    def create_developer_group(self, project_name):
        return self.create_group(project_name, Utils.DEVELOPER_SUFFIX)

    def create_group(self, project_name, suffix):
        # First try to get the group ID if the group already exists
        response = requests.get(
            f"{self.api_url}/v1/identity/group/name/{project_name}-{suffix}",
            headers={"X-Vault-Token": self.token},
        )
        if response.ok:
            return response.json()["data"]["id"]

        # If the group doesn't exist, create it
        print(f"Creating group for {project_name}-{suffix}")
        response = requests.post(
            f"{self.api_url}/v1/identity/group",
            json={
                "name": f"{project_name}-{suffix}",
                "type": "external",
                "policies": [f"{project_name}-{suffix}"],
            },
            headers={"X-Vault-Token": self.token},
        )
        return response.json()["data"]["id"]

    def get_oidc_mount_accessor(self):
        response = requests.get(
            f"{self.api_url}/v1/sys/auth",
            headers={"X-Vault-Token": self.token},
        )
        return response.json()["data"]["oidc/"]["accessor"]

    def create_group_alias(self, group_alias, group_id):
        print(f"Group ID: {group_id}")
        print(f"Creating group alias for {group_alias}")
        response = requests.post(
            f"{self.api_url}/v1/identity/group-alias",
            json={
                "name": group_alias,
                "mount_accessor": self.get_oidc_mount_accessor(),
                "canonical_id": group_id,
            },
            headers={"X-Vault-Token": self.token},
        )
        Utils.print_response(response)
