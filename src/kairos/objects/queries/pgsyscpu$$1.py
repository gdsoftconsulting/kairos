null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "PGSYSCPU$$1",
            "collections": [
                "vpsutil_cpu_times"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, 'USER_TIME'::text as label, usr as value from vpsutil_cpu_times union all select timestamp, 'SYS_TIME'::text as label, sys as value from vpsutil_cpu_times union all select timestamp, 'IOWAIT_TIME'::text as label, iowait as value from vpsutil_cpu_times) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": false
        }
        super(UserObject, self).__init__(**object)
