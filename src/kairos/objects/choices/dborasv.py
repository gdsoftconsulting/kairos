class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORASV",
            "action": "dispchart",
            "chart": "DBORACHOOSESV",
            "query": "DBORASVCHOICE",
        }
        super(UserObject, self).__init__(**object)
