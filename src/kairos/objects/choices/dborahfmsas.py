class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAHFMSAS",
            "action": "dispchart",
            "chart": "DBORAHFMSAS",
            "query": "DBORAHFMSCHOICE",
        }
        super(UserObject, self).__init__(**object)
