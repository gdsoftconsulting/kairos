class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "SNAPPERWEVOID",
            "action": "dispchart",
            "chart": "SNAPPERWEVOID",
            "query": "SNAPPERWEVCHOICE",
        }
        super(UserObject, self).__init__(**object)
