null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "PGSYSREFTIME",
            "collections": ["vpsutil_cpu_times"],
            "request": "select distinct timestamp from vpsutil_cpu_times"
        }
        super(UserObject, self).__init__(**object)
