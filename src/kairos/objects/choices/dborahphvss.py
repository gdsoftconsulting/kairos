class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAHPHVSS",
            "action": "dispchart",
            "chart": "DBORAHPHVSS",
            "query": "DBORAHPHVCHOICE",
        }
        super(UserObject, self).__init__(**object)
