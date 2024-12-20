null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAASHSQLCHOICE",
            "collections": ["ORAHAS"],
            "request": "select distinct sql_id as label from ORAHAS where sql_id != '' order by label"
        }
        super(UserObject, self).__init__(**object)
