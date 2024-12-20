class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHTXOPN",
            "action": "dispchart",
            "chart": "DBORAASHTXOPN",
            "query": "DBORAASHTXCHOICE",
        }
        super(UserObject, self).__init__(**object)
