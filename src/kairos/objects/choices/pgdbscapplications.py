class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "PGDBSCAPPLICATIONS",
            "action": "dispchart",
            "chart": "PGDBSCAPPLICATIONS",
            "query": "PGDATABASECHOICE",
        }
        super(UserObject, self).__init__(**object)
