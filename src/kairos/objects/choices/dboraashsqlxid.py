class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHSQLXID",
            "action": "dispchart",
            "chart": "DBORAASHSQLXID",
            "query": "DBORAASHSQLCHOICE",
        }
        super(UserObject, self).__init__(**object)
