null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "NMONREFTIME",
            "collections": ["NMONCPU"],
            "request": "select distinct timestamp from NMONCPU"
        }
        super(UserObject, self).__init__(**object)
