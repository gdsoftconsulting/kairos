class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "SNAPPERSESWEV",
            "action": "dispchart",
            "chart": "SNAPPERSESWEV",
            "query": "SNAPPERSESCHOICE",
        }
        super(UserObject, self).__init__(**object)
