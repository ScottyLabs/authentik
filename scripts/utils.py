class Utils:
    @staticmethod
    def print_response(response):
        print(response)
        try:
            print(response.json())
        except Exception:
            pass
        print()
