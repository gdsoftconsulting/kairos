class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "SNAPPERWEVSES",
            "action": "dispchart",
            "chart": "SNAPPERWEVSES",
            "query": "SNAPPERWEVCHOICE",
        }
        super(UserObject, self).__init__(**object)
