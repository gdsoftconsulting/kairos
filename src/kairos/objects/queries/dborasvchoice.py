null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORASVCHOICE",
            "collections": ["DBORASRV"],
            "request": "select distinct service as label from DBORASRV order by label"
        }
        super(UserObject, self).__init__(**object)
