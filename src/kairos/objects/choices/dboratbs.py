class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORATBS",
            "action": "dispchart",
            "chart": "DBORACHOOSETBS",
            "query": "DBORATBSCHOICE",
        }
        super(UserObject, self).__init__(**object)
