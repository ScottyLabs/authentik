from hashicorp import HashicorpManager

project_name = input("Enter the project name: ").strip().lower()
hashicorp_manager = HashicorpManager(project_name)
hashicorp_manager.create_admin_policy(project_name)
group_id = hashicorp_manager.get_group_id(project_name, hashicorp_manager.ADMIN_SUFFIX)
hashicorp_manager.create_group(project_name, hashicorp_manager.ADMIN_SUFFIX, group_id)

hashicorp_manager.create_developer_policy(project_name)
group_id = hashicorp_manager.get_group_id(
    project_name, hashicorp_manager.DEVELOPER_SUFFIX
)
hashicorp_manager.create_group(
    project_name, hashicorp_manager.DEVELOPER_SUFFIX, group_id
)
