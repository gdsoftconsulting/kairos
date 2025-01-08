class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "EBSQUEPRGW",
            "action": "dispchart",
            "chart": "EBSQUEPRGW",
            "query": "EBSQUECHOICE",
        }
        super(UserObject, self).__init__(**object)
