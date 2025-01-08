class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHSQLTM",
            "action": "dispchart",
            "chart": "DBORAASHSQLTM",
            "query": "DBORAASHSQLCHOICE",
        }
        super(UserObject, self).__init__(**object)
