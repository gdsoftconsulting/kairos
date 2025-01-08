class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAHSQLAS",
            "action": "dispchart",
            "chart": "DBORAHSQLAS",
            "query": "DBORAHSQLSCHOICE",
        }
        super(UserObject, self).__init__(**object)
