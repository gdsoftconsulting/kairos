null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORASTACHOICE",
            "collections": ["DBORASTA"],
            "request": "select distinct statistic as label from DBORASTA order by label"
        }
        super(UserObject, self).__init__(**object)
