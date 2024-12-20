class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAHSQLSS",
            "action": "dispchart",
            "chart": "DBORAHSQLSS",
            "query": "DBORAHSQLSCHOICE",
        }
        super(UserObject, self).__init__(**object)
