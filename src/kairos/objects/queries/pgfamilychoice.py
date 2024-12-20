null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "PGFAMILYCHOICE",
            "collections": ["vpsutil_processes"],
            "request": "select distinct cmdline as label from vpsutil_processes order by label"
        }
        super(UserObject, self).__init__(**object)
