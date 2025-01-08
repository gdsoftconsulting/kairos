class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "EBSNODEXER",
            "action": "dispchart",
            "chart": "EBSNODEXER",
            "query": "EBSNODCHOICE",
        }
        super(UserObject, self).__init__(**object)
