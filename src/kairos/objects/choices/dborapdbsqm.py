class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAPDBSQM",
            "action": "dispchart",
            "chart": "DBORAPDBSQM",
            "query": "DBORAPDBCHOICE",
        }
        super(UserObject, self).__init__(**object)
