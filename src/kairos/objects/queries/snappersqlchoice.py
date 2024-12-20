null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "SNAPPERSQLCHOICE",
            "collections": ["SNAPPER"],
            "request": "select distinct sql_id as label from SNAPPER where sql_id != '' order by label"
        }
        super(UserObject, self).__init__(**object)
