null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAHHELP",
            "collections": ["ORAHQT"],
            "nocache": True,
            "request": "select distinct sql_id as key, sql_text as value from ORAHQT where sql_id = '%(DBORAHELP)s'"
        }
        super(UserObject, self).__init__(**object)
