class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHPDBSES",
            "action": "dispchart",
            "chart": "DBORAASHPDBSES",
            "query": "DBORAASHPDBCHOICE",
        }
        super(UserObject, self).__init__(**object)
