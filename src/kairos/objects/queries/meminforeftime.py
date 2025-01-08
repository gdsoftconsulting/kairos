null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "MEMINFOREFTIME",
            "collections": ["MEMINFO"],
            "request": "select distinct timestamp from MEMINFO"
        }
        super(UserObject, self).__init__(**object)
