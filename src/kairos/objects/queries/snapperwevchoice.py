null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "SNAPPERWEVCHOICE",
            "collections": ["SNAPPER"],
            "request": "select distinct event as label from SNAPPER where event  != 'ON CPU' order by label"
        }
        super(UserObject, self).__init__(**object)
