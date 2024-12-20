class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "BOREPUSR",
            "action": "dispchart",
            "chart": "BOREPUSR",
            "query": "BOREPCHOICE",
        }
        super(UserObject, self).__init__(**object)
