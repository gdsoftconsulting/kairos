null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAHHELPF",
            "collections": ["ORAHQT", "ORAHQS"],
            "nocache": True,
            "request": "select distinct '%(DBORAHELPF)s' as key, sql_text as value from ORAHQT where sql_id in (select sql_id from ORAHQS where force_matching_signature = '%(DBORAHELPF)s')"
        }
        super(UserObject, self).__init__(**object)
