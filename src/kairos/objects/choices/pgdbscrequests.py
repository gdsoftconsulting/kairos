class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "PGDBSCREQUESTS",
            "action": "dispchart",
            "chart": "PGDBSCREQUESTS",
            "query": "PGDATABASECHOICE",
        }
        super(UserObject, self).__init__(**object)
