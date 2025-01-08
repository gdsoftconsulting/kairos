null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAASHMODCHOICE",
            "collections": ["ORAHAS"],
            "request": "select distinct module as label from ORAHAS where module != '' order by label"
        }
        super(UserObject, self).__init__(**object)
