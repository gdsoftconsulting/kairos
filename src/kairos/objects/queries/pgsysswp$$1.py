null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "PGSYSSWP$$1",
            "collections": [
                "vpsutil_swap_memory"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, 'Total size'::text as label, total::real as value from vpsutil_swap_memory union all select timestamp, 'Used size'::text as label, used::real as value from vpsutil_swap_memory) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": false
        }
        super(UserObject, self).__init__(**object)
