class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "PGDBSCTRANSACTIONS",
            "action": "dispchart",
            "chart": "PGDBSCTRANSACTIONS",
            "query": "PGDATABASECHOICE",
        }
        super(UserObject, self).__init__(**object)
