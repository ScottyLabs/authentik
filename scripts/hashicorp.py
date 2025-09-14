import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("HASHICORP_API_TOKEN")
api_url = os.getenv("HASHICORP_API_URL")

ADMIN_SUFFIX = "admins"
DEVELOPER_SUFFIX = "devs"


def create_admin_policy(project_name):
    print(f"Creating admin policy for {project_name}")
    policy = """\
path "/ScottyLabs/data/{project_name}/*" {{
    capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}}

path "/ScottyLabs/metadata/{project_name}/*" {{
    capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}}\
""".format(project_name=project_name)

    response = requests.post(
        f"{api_url}/v1/sys/policy/{project_name}-{ADMIN_SUFFIX}",
        json={"policy": policy},
        headers={"X-Vault-Token": token},
    )
    print(response)


def create_developer_policy(project_name):
    print(f"Creating developer policy for {project_name}")
    policy = """\
path "/ScottyLabs/data/{project_name}/*" {{
    capabilities = ["read", "list"]
}}\
""".format(project_name=project_name)
    response = requests.post(
        f"{api_url}/v1/sys/policy/{project_name}-{DEVELOPER_SUFFIX}",
        json={"policy": policy},
        headers={"X-Vault-Token": token},
    )
    try:
        print(response.json())
    except Exception:
        print(response)


def get_group_id(project_name, suffix):
    # First try to get the group ID if the group already exists
    response = requests.get(
        f"{api_url}/v1/identity/group/name/{project_name}-{suffix}",
        headers={"X-Vault-Token": token},
    )
    if response.ok:
        return response.json()["data"]["id"]

    # If the group doesn't exist, create it
    print(f"Creating group for {project_name}-{suffix}")
    response = requests.post(
        f"{api_url}/v1/identity/group",
        json={
            "name": f"{project_name}-{suffix}",
            "type": "external",
            "policies": [f"{project_name}-{suffix}"],
        },
        headers={"X-Vault-Token": token},
    )
    return response.json()["data"]["id"]


def get_oidc_mount_accessor():
    response = requests.get(
        f"{api_url}/v1/sys/auth",
        headers={"X-Vault-Token": token},
    )
    return response.json()["data"]["oidc/"]["accessor"]


def create_group(project_name, suffix, group_id):
    print(f"Group ID: {group_id}")
    print(f"Creating group alias for {project_name}-{suffix}")
    response = requests.post(
        f"{api_url}/v1/identity/group-alias",
        json={
            "name": f"{project_name}-{suffix}",
            "mount_accessor": get_oidc_mount_accessor(),
            "canonical_id": group_id,
        },
        headers={"X-Vault-Token": token},
    )
    try:
        print(response.json())
    except Exception:
        print(response)


if __name__ == "__main__":
    project_name = input("Enter the project name: ").strip().lower()
    create_admin_policy(project_name)
    group_id = get_group_id(project_name, ADMIN_SUFFIX)
    create_group(project_name, ADMIN_SUFFIX, group_id)

    create_developer_policy(project_name)
    group_id = get_group_id(project_name, DEVELOPER_SUFFIX)
    create_group(project_name, DEVELOPER_SUFFIX, group_id)
