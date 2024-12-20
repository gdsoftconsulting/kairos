class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORABUFPOOL",
            "action": "dispchart",
            "chart": "DBORACHOOSEBUFPOOL",
            "query": "DBORABUFPOOLCHOICE",
        }
        super(UserObject, self).__init__(**object)
