class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "EBSNODPRGR",
            "action": "dispchart",
            "chart": "EBSNODPRGR",
            "query": "EBSNODCHOICE",
        }
        super(UserObject, self).__init__(**object)
