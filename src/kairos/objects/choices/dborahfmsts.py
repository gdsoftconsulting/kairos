class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAHFMSTS",
            "action": "dispchart",
            "chart": "DBORAHFMSTS",
            "query": "DBORAHFMSCHOICE",
        }
        super(UserObject, self).__init__(**object)
