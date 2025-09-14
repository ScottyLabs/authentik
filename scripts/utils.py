class Utils:
    ADMIN_SUFFIX = "admins"
    DEVELOPER_SUFFIX = "devs"

    @staticmethod
    def print_response(response):
        print(response)
        try:
            print(response.json())
        except Exception:
            pass
        print()
