null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "PGSYSDSKWRITECOUNT$$1",
            "collections": [
                "vpsutil_disk_io_counters"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, disk as label, write_count as value from vpsutil_disk_io_counters) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": true
        }
        super(UserObject, self).__init__(**object)