null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAHSQLSCHOICE",
            "collections": ["ORAHQS"],
            "request": "select distinct sql_id as label from ORAHQS order by label"
        }
        super(UserObject, self).__init__(**object)
