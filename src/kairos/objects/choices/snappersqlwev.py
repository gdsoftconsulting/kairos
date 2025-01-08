class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "SNAPPERSQLWEV",
            "action": "dispchart",
            "chart": "SNAPPERSQLWEV",
            "query": "SNAPPERSQLCHOICE",
        }
        super(UserObject, self).__init__(**object)
