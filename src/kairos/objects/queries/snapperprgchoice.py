null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "SNAPPERPRGCHOICE",
            "collections": ["SNAPPER"],
            "request": "select distinct program as label from SNAPPER where program != '' order by label"
        }
        super(UserObject, self).__init__(**object)
