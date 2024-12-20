class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAHPHVTS",
            "action": "dispchart",
            "chart": "DBORAHPHVTS",
            "query": "DBORAHPHVCHOICE",
        }
        super(UserObject, self).__init__(**object)
