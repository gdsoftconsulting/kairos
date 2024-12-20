class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "PGDBSCWAITTYPES",
            "action": "dispchart",
            "chart": "PGDBSCWAITTYPES",
            "query": "PGDATABASECHOICE",
        }
        super(UserObject, self).__init__(**object)
