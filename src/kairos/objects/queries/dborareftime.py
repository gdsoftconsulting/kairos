null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAREFTIME",
            "collections": ["DBORAMISC"],
            "request": "select distinct timestamp from DBORAMISC"
        }
        super(UserObject, self).__init__(**object)
