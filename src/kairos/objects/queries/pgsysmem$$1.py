null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "PGSYSMEM$$1",
            "collections": [
                "vpsutil_virt_memory"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, 'Total size'::text as label, total::real as value from vpsutil_virt_memory union all select timestamp, 'Available size'::text as label, available::real as value from vpsutil_virt_memory union all select timestamp, 'Used size'::text as label, used::real as value from vpsutil_virt_memory union all select timestamp, 'Free size'::text as label, free::real as value from vpsutil_virt_memory union all select timestamp, 'Active size'::text as label, active::real as value from vpsutil_virt_memory union all select timestamp, 'Inactive size'::text as label, inactive::real as value from vpsutil_virt_memory union all select timestamp, 'Buffers size'::text as label, buffers::real as value from vpsutil_virt_memory union all select timestamp, 'Cached size'::text as label, cached::real as value from vpsutil_virt_memory) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": false
        }
        super(UserObject, self).__init__(**object)
