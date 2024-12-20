class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "SNAPPERPRGSES",
            "action": "dispchart",
            "chart": "SNAPPERPRGSES",
            "query": "SNAPPERPRGCHOICE",
        }
        super(UserObject, self).__init__(**object)
