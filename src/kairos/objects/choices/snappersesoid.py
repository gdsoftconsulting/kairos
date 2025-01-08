class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "SNAPPERSESOID",
            "action": "dispchart",
            "chart": "SNAPPERSESOID",
            "query": "SNAPPERSESCHOICE",
        }
        super(UserObject, self).__init__(**object)
