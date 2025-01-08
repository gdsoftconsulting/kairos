class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAHPHVAX",
            "action": "dispchart",
            "chart": "DBORAHPHVAX",
            "query": "DBORAHPHVCHOICE",
        }
        super(UserObject, self).__init__(**object)
