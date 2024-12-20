null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "BOUSRCHOICE",
            "collections": ["BO"],
            "request": "select distinct user_name as label from BO order by label"
        }
        super(UserObject, self).__init__(**object)
