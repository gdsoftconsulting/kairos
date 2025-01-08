class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHSQLEPO",
            "action": "dispchart",
            "chart": "DBORAASHSQLEPO",
            "query": "DBORAASHSQLCHOICE",
        }
        super(UserObject, self).__init__(**object)
