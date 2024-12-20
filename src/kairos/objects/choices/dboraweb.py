class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAWEB",
            "action": "dispchart",
            "chart": "DBORACHOOSEWEB",
            "query": "DBORAWEBCHOICE",
        }
        super(UserObject, self).__init__(**object)
