class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "PGDBSCWAITEVENTS",
            "action": "dispchart",
            "chart": "PGDBSCWAITEVENTS",
            "query": "PGDATABASECHOICE",
        }
        super(UserObject, self).__init__(**object)
