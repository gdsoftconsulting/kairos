class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "SNAPPERSCHSES",
            "action": "dispchart",
            "chart": "SNAPPERSCHSES",
            "query": "SNAPPERSCHCHOICE",
        }
        super(UserObject, self).__init__(**object)
