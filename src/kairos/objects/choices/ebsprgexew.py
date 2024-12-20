class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "EBSPRGEXEW",
            "action": "dispchart",
            "chart": "EBSPRGEXEW",
            "query": "EBSPRGCHOICE",
        }
        super(UserObject, self).__init__(**object)
