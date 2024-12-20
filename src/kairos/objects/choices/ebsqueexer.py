class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "EBSQUEEXER",
            "action": "dispchart",
            "chart": "EBSQUEEXER",
            "query": "EBSQUECHOICE",
        }
        super(UserObject, self).__init__(**object)
