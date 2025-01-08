class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAHSQLAX",
            "action": "dispchart",
            "chart": "DBORAHSQLAX",
            "query": "DBORAHSQLSCHOICE",
        }
        super(UserObject, self).__init__(**object)
