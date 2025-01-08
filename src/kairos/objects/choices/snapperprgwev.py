class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "SNAPPERPRGWEV",
            "action": "dispchart",
            "chart": "SNAPPERPRGWEV",
            "query": "SNAPPERPRGCHOICE",
        }
        super(UserObject, self).__init__(**object)
