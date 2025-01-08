class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAPDBSQR",
            "action": "dispchart",
            "chart": "DBORAPDBSQR",
            "query": "DBORAPDBCHOICE",
        }
        super(UserObject, self).__init__(**object)
