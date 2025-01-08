null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAWEHCHOICE",
            "collections": ["DBORAWEH"],
            "request": "select distinct event as label from DBORAWEH order by label"
        }
        super(UserObject, self).__init__(**object)
