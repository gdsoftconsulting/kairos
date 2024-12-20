class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "BOUSRREQ",
            "action": "dispchart",
            "chart": "BOUSRREQ",
            "query": "BOUSRCHOICE",
        }
        super(UserObject, self).__init__(**object)
