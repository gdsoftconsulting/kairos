null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "SNAPPERREFTIME",
            "collections": ["SNAPPER"],
            "request": "select distinct timestamp from SNAPPER"
        }
        super(UserObject, self).__init__(**object)
