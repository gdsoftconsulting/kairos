class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "EBSNODQUEW",
            "action": "dispchart",
            "chart": "EBSNODQUEW",
            "query": "EBSNODCHOICE",
        }
        super(UserObject, self).__init__(**object)
