class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "EBSPRGEXER",
            "action": "dispchart",
            "chart": "EBSPRGEXER",
            "query": "EBSPRGCHOICE",
        }
        super(UserObject, self).__init__(**object)
