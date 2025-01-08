class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "EBSQUEPRGR",
            "action": "dispchart",
            "chart": "EBSQUEPRGR",
            "query": "EBSQUECHOICE",
        }
        super(UserObject, self).__init__(**object)
