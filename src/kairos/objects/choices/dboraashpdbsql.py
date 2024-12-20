class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHPDBSQL",
            "action": "dispchart",
            "chart": "DBORAASHPDBSQL",
            "query": "DBORAASHPDBCHOICE",
        }
        super(UserObject, self).__init__(**object)
