class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORASGA",
            "action": "dispchart",
            "chart": "DBORACHOOSESGA",
            "query": "DBORASGACHOICE",
        }
        super(UserObject, self).__init__(**object)
