null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "PGSYSCHOOSEDISK$$1",
            "collections": [
                "vpsutil_disk_io_counters"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, avg(value) as value from (select timestamp, 'Average time per read'::text as label, (case when read_count = 0 then 0.0 else read_time * 1.0 / read_count end) as value from vpsutil_disk_io_counters where disk = '%(PGSYSDISK)s'::text union all select timestamp, 'Average time per write'::text as label, (case when write_count = 0 then 0.0 else write_time * 1.0 / write_count end) as value from vpsutil_disk_io_counters where disk = '%(PGSYSDISK)s'::text) as foo group by timestamp, label order by timestamp",
            "nocache": true,
            "filterable": false
        }
        super(UserObject, self).__init__(**object)
