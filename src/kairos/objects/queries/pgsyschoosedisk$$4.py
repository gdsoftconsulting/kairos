null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "PGSYSCHOOSEDISK$$4",
            "collections": [
                "vpsutil_disk_io_counters"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, avg(value) as value from (select timestamp, 'Average read count per second'::text as label, read_count as value from vpsutil_disk_io_counters where disk = '%(PGSYSDISK)s'::text union all select timestamp, 'Average write count per second'::text as label, write_count as value from vpsutil_disk_io_counters where disk = '%(PGSYSDISK)s'::text) as foo group by timestamp, label order by timestamp",
            "nocache": true,
            "filterable": false
        }
        super(UserObject, self).__init__(**object)
