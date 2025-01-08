null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAASHPRGCHOICE",
            "collections": ["ORAHAS"],
            "request": "select distinct program as label from ORAHAS where program != '' order by label"
        }
        super(UserObject, self).__init__(**object)
