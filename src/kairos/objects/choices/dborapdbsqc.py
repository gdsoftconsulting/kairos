class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAPDBSQC",
            "action": "dispchart",
            "chart": "DBORAPDBSQC",
            "query": "DBORAPDBCHOICE",
        }
        super(UserObject, self).__init__(**object)
