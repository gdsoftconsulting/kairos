null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "SARCPU$$1",
            "collections": [
                "SARU"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, 'sys'::text as label, sys as value from SARU where cpuid = 'all' union all select timestamp, 'usr'::text as label, usr as value from SARU where cpuid = 'all') as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": true
        }
        super(UserObject, self).__init__(**object)
