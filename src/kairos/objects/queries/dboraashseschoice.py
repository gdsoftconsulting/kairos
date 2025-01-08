null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAASHSESCHOICE",
            "collections": ["ORAHAS"],
            "request": "select distinct session_id||' - '||program as label from ORAHAS order by label"
        }
        super(UserObject, self).__init__(**object)
