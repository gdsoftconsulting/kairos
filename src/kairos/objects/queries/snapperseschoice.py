null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "SNAPPERSESCHOICE",
            "collections": ["SNAPPER"],
            "request": "select distinct sid||' - '||program as label from SNAPPER order by label"
        }
        super(UserObject, self).__init__(**object)
