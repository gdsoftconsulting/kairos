class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHMODSES",
            "action": "dispchart",
            "chart": "DBORAASHMODSES",
            "query": "DBORAASHMODCHOICE",
        }
        super(UserObject, self).__init__(**object)
