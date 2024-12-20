null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "SNAPPERSCHCHOICE",
            "collections": ["SNAPPER"],
            "request": "select distinct username as label from SNAPPER where username != '' order by label"
        }
        super(UserObject, self).__init__(**object)
