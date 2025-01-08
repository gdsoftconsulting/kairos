class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "TTSQLT",
            "action": "dispchart",
            "chart": "TTSQLT",
            "query": "TTSQLCHOICE",
        }
        super(UserObject, self).__init__(**object)
