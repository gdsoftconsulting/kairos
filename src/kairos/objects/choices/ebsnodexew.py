class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "EBSNODEXEW",
            "action": "dispchart",
            "chart": "EBSNODEXEW",
            "query": "EBSNODCHOICE",
        }
        super(UserObject, self).__init__(**object)
