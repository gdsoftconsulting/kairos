class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHPDBDBT",
            "action": "dispchart",
            "chart": "DBORAASHPDBDBT",
            "query": "DBORAASHPDBCHOICE",
        }
        super(UserObject, self).__init__(**object)
