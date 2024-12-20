class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHSESSQL",
            "action": "dispchart",
            "chart": "DBORAASHSESSQL",
            "query": "DBORAASHSESCHOICE",
        }
        super(UserObject, self).__init__(**object)
