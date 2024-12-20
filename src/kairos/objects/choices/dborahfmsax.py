class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAHFMSAX",
            "action": "dispchart",
            "chart": "DBORAHFMSAX",
            "query": "DBORAHFMSCHOICE",
        }
        super(UserObject, self).__init__(**object)
