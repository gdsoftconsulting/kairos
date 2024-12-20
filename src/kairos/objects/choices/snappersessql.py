class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "SNAPPERSESSQL",
            "action": "dispchart",
            "chart": "SNAPPERSESSQL",
            "query": "SNAPPERSESCHOICE",
        }
        super(UserObject, self).__init__(**object)
