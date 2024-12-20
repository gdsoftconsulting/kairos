class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHSQLPHV",
            "action": "dispchart",
            "chart": "DBORAASHSQLPHV",
            "query": "DBORAASHSQLCHOICE",
        }
        super(UserObject, self).__init__(**object)
