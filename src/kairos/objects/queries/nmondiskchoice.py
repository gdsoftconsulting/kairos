null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "NMONDISKCHOICE",
            "collections": ["NMONDISKREAD"],
            "request": "select distinct id as label from NMONDISKREAD order by label"
        }
        super(UserObject, self).__init__(**object)
