class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "SNAPPERSCHSQL",
            "action": "dispchart",
            "chart": "SNAPPERSCHSQL",
            "query": "SNAPPERSCHCHOICE",
        }
        super(UserObject, self).__init__(**object)
