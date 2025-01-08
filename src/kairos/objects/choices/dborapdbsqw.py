class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAPDBSQW",
            "action": "dispchart",
            "chart": "DBORAPDBSQW",
            "query": "DBORAPDBCHOICE",
        }
        super(UserObject, self).__init__(**object)
