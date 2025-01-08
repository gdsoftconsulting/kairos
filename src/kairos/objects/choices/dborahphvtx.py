class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAHPHVTX",
            "action": "dispchart",
            "chart": "DBORAHPHVTX",
            "query": "DBORAHPHVCHOICE",
        }
        super(UserObject, self).__init__(**object)
