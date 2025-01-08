null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "TTREFTIME",
            "collections": ["TTMISC"],
            "request": "select distinct timestamp from TTMISC"
        }
        super(UserObject, self).__init__(**object)
