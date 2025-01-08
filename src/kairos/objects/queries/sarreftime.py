null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "SARREFTIME",
            "collections": ["SARU"],
            "request": "select distinct timestamp from SARU"
        }
        super(UserObject, self).__init__(**object)
