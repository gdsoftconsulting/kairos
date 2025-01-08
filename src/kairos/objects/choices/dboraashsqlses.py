class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHSQLSES",
            "action": "dispchart",
            "chart": "DBORAASHSQLSES",
            "query": "DBORAASHSQLCHOICE",
        }
        super(UserObject, self).__init__(**object)
