class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "EBSPRGQUEW",
            "action": "dispchart",
            "chart": "EBSPRGQUEW",
            "query": "EBSPRGCHOICE",
        }
        super(UserObject, self).__init__(**object)
