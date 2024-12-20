class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "TTSQLE",
            "action": "dispchart",
            "chart": "TTSQLE",
            "query": "TTSQLCHOICE",
        }
        super(UserObject, self).__init__(**object)
