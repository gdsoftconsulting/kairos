class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "EBSPRGNODW",
            "action": "dispchart",
            "chart": "EBSPRGNODW",
            "query": "EBSPRGCHOICE",
        }
        super(UserObject, self).__init__(**object)
