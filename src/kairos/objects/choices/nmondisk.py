class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "NMONDISK",
            "action": "dispchart",
            "chart": "NMONDISK",
            "query": "NMONDISKCHOICE",
        }
        super(UserObject, self).__init__(**object)
