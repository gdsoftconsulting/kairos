class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "SNAPPERSCHWEV",
            "action": "dispchart",
            "chart": "SNAPPERSCHWEV",
            "query": "SNAPPERSCHCHOICE",
        }
        super(UserObject, self).__init__(**object)
