null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAWEBCHOICE",
            "collections": ["DBORAWEB"],
            "request": "select distinct event as label from DBORAWEB order by label"
        }
        super(UserObject, self).__init__(**object)
