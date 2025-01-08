class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAHPHVSX",
            "action": "dispchart",
            "chart": "DBORAHPHVSX",
            "query": "DBORAHPHVCHOICE",
        }
        super(UserObject, self).__init__(**object)
