class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAPDBSQE",
            "action": "dispchart",
            "chart": "DBORAPDBSQE",
            "query": "DBORAPDBCHOICE",
        }
        super(UserObject, self).__init__(**object)
