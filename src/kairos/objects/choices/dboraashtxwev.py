class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHTXWEV",
            "action": "dispchart",
            "chart": "DBORAASHTXWEV",
            "query": "DBORAASHTXCHOICE",
        }
        super(UserObject, self).__init__(**object)
