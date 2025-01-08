null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "VMSTATREFTIME",
            "collections": ["VMSTAT"],
            "request": "select distinct timestamp from VMSTAT"
        }
        super(UserObject, self).__init__(**object)
