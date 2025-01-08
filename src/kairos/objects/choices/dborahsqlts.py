class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAHSQLTS",
            "action": "dispchart",
            "chart": "DBORAHSQLTS",
            "query": "DBORAHSQLSCHOICE",
        }
        super(UserObject, self).__init__(**object)
