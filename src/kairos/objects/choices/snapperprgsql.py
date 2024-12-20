class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "SNAPPERPRGSQL",
            "action": "dispchart",
            "chart": "SNAPPERPRGSQL",
            "query": "SNAPPERPRGCHOICE",
        }
        super(UserObject, self).__init__(**object)
