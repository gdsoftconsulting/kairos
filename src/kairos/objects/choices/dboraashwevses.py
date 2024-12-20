class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHWEVSES",
            "action": "dispchart",
            "chart": "DBORAASHWEVSES",
            "query": "DBORAASHWEVCHOICE",
        }
        super(UserObject, self).__init__(**object)
