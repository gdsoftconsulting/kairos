null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "PGSYSCHOOSEFAMILY$$1",
            "collections": [
                "vpsutil_processes"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, 'USER_TIME'::text as label, usr::real as value from vpsutil_processes where cmdline = '%(PGSYSFAMILY)s'::text union all select timestamp, 'SYS_TIME'::text as label, sys::real as value from vpsutil_processes where cmdline = '%(PGSYSFAMILY)s'::text) as foo group by timestamp, label order by timestamp",
            "nocache": true,
            "filterable": false
        }
        super(UserObject, self).__init__(**object)
