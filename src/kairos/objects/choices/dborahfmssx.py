class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAHFMSSX",
            "action": "dispchart",
            "chart": "DBORAHFMSSX",
            "query": "DBORAHFMSCHOICE",
        }
        super(UserObject, self).__init__(**object)
