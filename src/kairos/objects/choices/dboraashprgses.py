class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHPRGSES",
            "action": "dispchart",
            "chart": "DBORAASHPRGSES",
            "query": "DBORAASHPRGCHOICE",
        }
        super(UserObject, self).__init__(**object)
