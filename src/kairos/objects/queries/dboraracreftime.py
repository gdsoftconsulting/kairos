null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORARACREFTIME",
            "collections": ["DBORARACMISC"],
            "request": "select distinct timestamp from DBORARACMISC"
        }
        super(UserObject, self).__init__(**object)
