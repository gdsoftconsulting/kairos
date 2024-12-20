null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "TTSTACHOICE",
            "collections": ["TTSTATS"],
            "request": "select distinct statistic as label from TTSTATS order by label"
        }
        super(UserObject, self).__init__(**object)
