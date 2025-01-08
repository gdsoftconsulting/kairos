null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAASHPDBCHOICE",
            "collections": ["ORAHAS"],
            "request": "select distinct con_name as label from ORAHAS order by label"
        }
        super(UserObject, self).__init__(**object)
