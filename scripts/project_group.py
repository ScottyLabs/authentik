from hashicorp import HashicorpManager
from authentik_group import AuthentikGroupManager
from utils import Utils

project_name = input("Enter the project name: ").strip().lower()

admin_group = f"{project_name}-{Utils.ADMIN_SUFFIX}"
developer_group = f"{project_name}-{Utils.DEVELOPER_SUFFIX}"

# Create Hashicorp groups
hashicorp_manager = HashicorpManager(project_name)

hashicorp_manager.create_admin_policy(project_name)
admin_group_id = hashicorp_manager.create_admin_group(project_name)
hashicorp_manager.create_group_alias(admin_group, admin_group_id)

hashicorp_manager.create_developer_policy(project_name)
developer_group_id = hashicorp_manager.create_developer_group(project_name)
hashicorp_manager.create_group_alias(developer_group, developer_group_id)

# Create Authentik groups
authentik_group_manager = AuthentikGroupManager()
authentik_group_manager.create_authentik_group(admin_group)
authentik_group_manager.create_authentik_group(developer_group)
