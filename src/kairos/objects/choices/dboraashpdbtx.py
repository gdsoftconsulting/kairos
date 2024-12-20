class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHPDBTX",
            "action": "dispchart",
            "chart": "DBORAASHPDBTX",
            "query": "DBORAASHPDBCHOICE",
        }
        super(UserObject, self).__init__(**object)
