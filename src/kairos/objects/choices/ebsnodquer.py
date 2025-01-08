class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "EBSNODQUER",
            "action": "dispchart",
            "chart": "EBSNODQUER",
            "query": "EBSNODCHOICE",
        }
        super(UserObject, self).__init__(**object)
