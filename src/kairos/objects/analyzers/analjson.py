
class UserObject(dict):
    def __init__(self):
        object = {
            "type": "analyzer",
            "id": "ANALJSON",
            "content": "json"
        }
        super(UserObject, self).__init__(**object)
