null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAASHTXCHOICE",
            "collections": ["ORAHAS"],
            "request": "select distinct xid as label from ORAHAS order by label"
        }
        super(UserObject, self).__init__(**object)
