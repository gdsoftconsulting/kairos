null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAWEVCHOICE",
            "collections": ["DBORAWEV"],
            "request": "select distinct event as label from DBORAWEV order by label"
        }
        super(UserObject, self).__init__(**object)
