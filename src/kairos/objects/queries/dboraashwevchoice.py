null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAASHWEVCHOICE",
            "collections": ["ORAHAS"],
            "request": "select distinct event as label from ORAHAS where session_state = 'WAITING' order by label"
        }
        super(UserObject, self).__init__(**object)
