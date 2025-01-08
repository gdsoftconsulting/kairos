class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "SNAPPERSQLSES",
            "action": "dispchart",
            "chart": "SNAPPERSQLSES",
            "query": "SNAPPERSQLCHOICE",
        }
        super(UserObject, self).__init__(**object)
