class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAWEV",
            "action": "dispchart",
            "chart": "DBORACHOOSEWEV",
            "query": "DBORAWEVCHOICE",
        }
        super(UserObject, self).__init__(**object)
