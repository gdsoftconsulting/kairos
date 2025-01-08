class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "SNAPPERSQLOID",
            "action": "dispchart",
            "chart": "SNAPPERSQLOID",
            "query": "SNAPPERSQLCHOICE",
        }
        super(UserObject, self).__init__(**object)
