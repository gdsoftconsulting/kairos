null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "BOREPCHOICE",
            "collections": ["BO"],
            "request": "select distinct report as label from BO order by label"
        }
        super(UserObject, self).__init__(**object)
