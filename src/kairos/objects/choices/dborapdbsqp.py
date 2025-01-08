class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAPDBSQP",
            "action": "dispchart",
            "chart": "DBORAPDBSQP",
            "query": "DBORAPDBCHOICE",
        }
        super(UserObject, self).__init__(**object)
