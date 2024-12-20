class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "TTSTA",
            "action": "dispchart",
            "chart": "TTSTA",
            "query": "TTSTACHOICE",
        }
        super(UserObject, self).__init__(**object)
