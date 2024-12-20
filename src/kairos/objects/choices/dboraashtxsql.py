class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHTXSQL",
            "action": "dispchart",
            "chart": "DBORAASHTXSQL",
            "query": "DBORAASHTXCHOICE",
        }
        super(UserObject, self).__init__(**object)
