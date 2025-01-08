null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAHHELPP",
            "collections": ["ORAHQT", "ORAHQS"],
            "nocache": True,
            "request": "select distinct '%(DBORAHELPP)s' as key, sql_text as value from ORAHQT where sql_id in (select sql_id from ORAHQS where plan_hash_value = '%(DBORAHELPP)s')"
        }
        super(UserObject, self).__init__(**object)
