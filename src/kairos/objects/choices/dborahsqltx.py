class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAHSQLTX",
            "action": "dispchart",
            "chart": "DBORAHSQLTX",
            "query": "DBORAHSQLSCHOICE",
        }
        super(UserObject, self).__init__(**object)
