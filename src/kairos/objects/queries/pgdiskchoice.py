null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "PGDISKCHOICE",
            "collections": ["vpsutil_disk_io_counters"],
            "request": "select distinct disk  as label from vpsutil_disk_io_counters order by label"
        }
        super(UserObject, self).__init__(**object)
