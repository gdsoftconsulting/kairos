class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "EBSQUENODW",
            "action": "dispchart",
            "chart": "EBSQUENODW",
            "query": "EBSQUECHOICE",
        }
        super(UserObject, self).__init__(**object)
