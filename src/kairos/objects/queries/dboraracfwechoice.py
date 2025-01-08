null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORARACFWECHOICE",
            "collections": ["DBORARACTTFE"],
            "request": "select distinct event as label from DBORARACTTFE order by label"
        }
        super(UserObject, self).__init__(**object)
