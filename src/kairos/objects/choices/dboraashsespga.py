class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHSESPGA",
            "action": "dispchart",
            "chart": "DBORAASHSESPGA",
            "query": "DBORAASHSESCHOICE",
        }
        super(UserObject, self).__init__(**object)
