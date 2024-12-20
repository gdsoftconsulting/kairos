class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAPDBSQV",
            "action": "dispchart",
            "chart": "DBORAPDBSQV",
            "query": "DBORAPDBCHOICE",
        }
        super(UserObject, self).__init__(**object)
