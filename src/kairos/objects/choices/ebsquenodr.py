class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "EBSQUENODR",
            "action": "dispchart",
            "chart": "EBSQUENODR",
            "query": "EBSQUECHOICE",
        }
        super(UserObject, self).__init__(**object)
