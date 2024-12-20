null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAHELP",
            "collections": ["DBORAREQ"],
            "nocache": True,
            "request": "select distinct sqlid as key, request as value from DBORAREQ where sqlid = '%(DBORAHELP)s'"
        }
        super(UserObject, self).__init__(**object)
