class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "SNAPPERWEVSQL",
            "action": "dispchart",
            "chart": "SNAPPERWEVSQL",
            "query": "SNAPPERWEVCHOICE",
        }
        super(UserObject, self).__init__(**object)
