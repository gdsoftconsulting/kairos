class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "BOUSRREP",
            "action": "dispchart",
            "chart": "BOUSRREP",
            "query": "BOUSRCHOICE",
        }
        super(UserObject, self).__init__(**object)
