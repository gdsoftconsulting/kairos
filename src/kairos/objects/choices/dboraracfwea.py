class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORARACFWEA",
            "action": "dispchart",
            "chart": "DBORARACFWEA",
            "query": "DBORARACFWECHOICE",
        }
        super(UserObject, self).__init__(**object)
