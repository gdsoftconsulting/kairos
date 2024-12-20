class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHMODSQL",
            "action": "dispchart",
            "chart": "DBORAASHMODSQL",
            "query": "DBORAASHMODCHOICE",
        }
        super(UserObject, self).__init__(**object)
