null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "EBSPRGCHOICE",
            "collections": ["EBS12CM"],
            "request": "select distinct prg_name as label from EBS12CM order by label"
        }
        super(UserObject, self).__init__(**object)
