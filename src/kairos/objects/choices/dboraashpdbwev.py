class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHPDBWEV",
            "action": "dispchart",
            "chart": "DBORAASHPDBWEV",
            "query": "DBORAASHPDBCHOICE",
        }
        super(UserObject, self).__init__(**object)
