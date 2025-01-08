class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "PGSYSCOMMAND",
            "action": "dispchart",
            "chart": "PGSYSCHOOSECOMMAND",
            "query": "PGCOMMANDCHOICE",
        }
        super(UserObject, self).__init__(**object)
