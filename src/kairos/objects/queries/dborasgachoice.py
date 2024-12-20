null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORASGACHOICE",
            "collections": ["DBORASGA"],
            "request": "select distinct pool||' '||name as label from DBORASGA order by label"
        }
        super(UserObject, self).__init__(**object)
