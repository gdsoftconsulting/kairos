class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAHPHVAS",
            "action": "dispchart",
            "chart": "DBORAHPHVAS",
            "query": "DBORAHPHVCHOICE",
        }
        super(UserObject, self).__init__(**object)
