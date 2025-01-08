class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "PGSYSPROCESS",
            "action": "dispchart",
            "chart": "PGSYSCHOOSEPROCESS",
            "query": "PGPROCESSCHOICE",
        }
        super(UserObject, self).__init__(**object)
