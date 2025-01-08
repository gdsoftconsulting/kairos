class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "EBSPRGNODR",
            "action": "dispchart",
            "chart": "EBSPRGNODR",
            "query": "EBSPRGCHOICE",
        }
        super(UserObject, self).__init__(**object)
