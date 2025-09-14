import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("AUTHENTIK_API_TOKEN")
url = os.getenv("AUTHENTIK_API_URL")
super_user_group_id = os.getenv("SUPER_USER_GROUP_ID")


def get_user(user_andrew_id):
    get_user_url = f"{url}/api/v3/core/users/?email={user_andrew_id}@andrew.cmu.edu"
    response = requests.get(
        get_user_url,
        headers={"Authorization": f"Bearer {token}"},
    )
    return response.json()


def add_user_to_super_user(user_uuid):
    add_user_to_super_user_url = (
        f"{url}/api/v3/core/groups/{super_user_group_id}/add_user/"
    )
    response = requests.post(
        add_user_to_super_user_url,
        json={"pk": user_uuid},
        headers={"Authorization": f"Bearer {token}"},
    )
    if not response.ok:
        print(f"ERROR: Failed to add user {user_uuid} to super user group")
        print(response)
        return

    print(f"SUCCESS: Added user {user_uuid} to super user group")


if __name__ == "__main__":
    andrew_id = input(
        "Enter the Andrew ID of the user to add to the super user group: "
    )
    user_response = get_user(andrew_id)
    if len(user_response["results"]) == 0:
        print("ERROR: Andrew ID not found")
        exit()

    if len(user_response["results"]) > 1:
        print("ERROR: Multiple users found for the same Andrew ID")
        exit()

    user_uuid = user_response["results"][0]["pk"]
    add_user_to_super_user(user_uuid)
