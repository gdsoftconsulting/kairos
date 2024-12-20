class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAHSQLSX",
            "action": "dispchart",
            "chart": "DBORAHSQLSX",
            "query": "DBORAHSQLSCHOICE",
        }
        super(UserObject, self).__init__(**object)
