class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHWEVP1",
            "action": "dispchart",
            "chart": "DBORAASHWEVP1",
            "query": "DBORAASHWEVCHOICE",
        }
        super(UserObject, self).__init__(**object)
