null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "PGSYSCHOOSEDISK$$3",
            "collections": [
                "vpsutil_disk_io_counters"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, avg(value) as value from (select timestamp, 'Average read volume per second'::text as label, read_bytes as value from vpsutil_disk_io_counters where disk = '%(PGSYSDISK)s'::text union all select timestamp, 'Average write volume per second'::text as label, write_bytes as value from vpsutil_disk_io_counters where disk = '%(PGSYSDISK)s'::text) as foo group by timestamp, label order by timestamp",
            "nocache": true,
            "filterable": false
        }
        super(UserObject, self).__init__(**object)
