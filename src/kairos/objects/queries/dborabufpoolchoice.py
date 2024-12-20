null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORABUFPOOLCHOICE",
            "collections": ["DBORABPA"],
            "request": "select distinct bufpool as label from DBORABPA order by label"
        }
        super(UserObject, self).__init__(**object)
