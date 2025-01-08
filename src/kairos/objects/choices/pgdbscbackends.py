class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "PGDBSCBACKENDS",
            "action": "dispchart",
            "chart": "PGDBSCBACKENDS",
            "query": "PGDATABASECHOICE",
        }
        super(UserObject, self).__init__(**object)
