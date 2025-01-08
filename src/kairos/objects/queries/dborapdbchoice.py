null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAPDBCHOICE",
            "collections": ["DBORAINFO"],
            "request": "select distinct  cname as label from DBORAINFO order by label"
        }
        super(UserObject, self).__init__(**object)
