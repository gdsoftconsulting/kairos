class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAPDBSQX",
            "action": "dispchart",
            "chart": "DBORAPDBSQX",
            "query": "DBORAPDBCHOICE",
        }
        super(UserObject, self).__init__(**object)
