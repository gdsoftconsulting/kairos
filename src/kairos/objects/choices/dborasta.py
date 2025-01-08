class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORASTA",
            "action": "dispchart",
            "chart": "DBORACHOOSESTA",
            "query": "DBORASTACHOICE",
        }
        super(UserObject, self).__init__(**object)
