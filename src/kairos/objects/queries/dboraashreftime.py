null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAASHREFTIME",
            "collections": ["ORAHAS"],
            "request": "select distinct timestamp from ORAHAS"
        }
        super(UserObject, self).__init__(**object)
