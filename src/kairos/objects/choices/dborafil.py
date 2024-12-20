class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAFIL",
            "action": "dispchart",
            "chart": "DBORACHOOSEFIL",
            "query": "DBORAFILCHOICE",
        }
        super(UserObject, self).__init__(**object)
