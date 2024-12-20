class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHSQLTMP",
            "action": "dispchart",
            "chart": "DBORAASHSQLTMP",
            "query": "DBORAASHSQLCHOICE",
        }
        super(UserObject, self).__init__(**object)
