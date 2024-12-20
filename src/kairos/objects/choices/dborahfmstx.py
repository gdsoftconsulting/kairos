class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAHFMSTX",
            "action": "dispchart",
            "chart": "DBORAHFMSTX",
            "query": "DBORAHFMSCHOICE",
        }
        super(UserObject, self).__init__(**object)
