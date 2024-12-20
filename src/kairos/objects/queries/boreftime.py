null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "BOREFTIME",
            "collections": ["BO"],
            "request": "select distinct timestamp from BO"
        }
        super(UserObject, self).__init__(**object)
