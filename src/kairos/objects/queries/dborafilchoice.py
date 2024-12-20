null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAFILCHOICE",
            "collections": ["DBORAFIL"],
            "request": "select distinct file as label from DBORAFIL order by label"
        }
        super(UserObject, self).__init__(**object)
