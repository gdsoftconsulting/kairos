class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAWEH",
            "action": "dispchart",
            "chart": "DBORACHOOSEWEH",
            "query": "DBORAWEHCHOICE",
        }
        super(UserObject, self).__init__(**object)
