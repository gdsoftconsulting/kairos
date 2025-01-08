class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHSESTMP",
            "action": "dispchart",
            "chart": "DBORAASHSESTMP",
            "query": "DBORAASHSESCHOICE",
        }
        super(UserObject, self).__init__(**object)
