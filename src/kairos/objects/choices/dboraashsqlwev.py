class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHSQLWEV",
            "action": "dispchart",
            "chart": "DBORAASHSQLWEV",
            "query": "DBORAASHSQLCHOICE",
        }
        super(UserObject, self).__init__(**object)
