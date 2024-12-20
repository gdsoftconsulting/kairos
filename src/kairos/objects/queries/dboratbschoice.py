null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORATBSCHOICE",
            "collections": ["DBORATBS"],
            "request": "select distinct tablespace as label from DBORATBS order by label"
        }
        super(UserObject, self).__init__(**object)
