class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "EBSPRGQUER",
            "action": "dispchart",
            "chart": "EBSPRGQUER",
            "query": "EBSPRGCHOICE",
        }
        super(UserObject, self).__init__(**object)
