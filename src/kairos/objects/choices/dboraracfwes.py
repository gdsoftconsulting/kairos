class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORARACFWES",
            "action": "dispchart",
            "chart": "DBORARACFWES",
            "query": "DBORARACFWECHOICE",
        }
        super(UserObject, self).__init__(**object)
