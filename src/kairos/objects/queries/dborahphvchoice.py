null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAHPHVCHOICE",
            "collections": ["ORAHQS"],
            "request": "select distinct plan_hash_value as label from ORAHQS order by label"
        }
        super(UserObject, self).__init__(**object)
