class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHWEVSQL",
            "action": "dispchart",
            "chart": "DBORAASHWEVSQL",
            "query": "DBORAASHWEVCHOICE",
        }
        super(UserObject, self).__init__(**object)
