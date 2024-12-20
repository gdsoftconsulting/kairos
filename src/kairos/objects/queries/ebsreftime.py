null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "EBSREFTIME",
            "collections": ["EBS12CM"],
            "request": "select distinct timestamp from EBS12CM"
        }
        super(UserObject, self).__init__(**object)
