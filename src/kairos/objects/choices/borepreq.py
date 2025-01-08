class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "BOREPREQ",
            "action": "dispchart",
            "chart": "BOREPREQ",
            "query": "BOREPCHOICE",
        }
        super(UserObject, self).__init__(**object)
