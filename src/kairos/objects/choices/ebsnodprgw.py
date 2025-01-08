class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "EBSNODPRGW",
            "action": "dispchart",
            "chart": "EBSNODPRGW",
            "query": "EBSNODCHOICE",
        }
        super(UserObject, self).__init__(**object)
