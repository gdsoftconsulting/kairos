null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "SARIOS$$1",
            "collections": [
                "SARB"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, 'lwrite'::text as label, lwrite as value from SARB union all select timestamp, 'lread'::text as label, lread as value from SARB union all select timestamp, 'pwrite'::text as label, pwrite as value from SARB union all select timestamp, 'pread'::text as label, pread as value from SARB union all select timestamp, 'bwrite'::text as label, bwrite as value from SARB union all select timestamp, 'bread'::text as label, bread as value from SARB) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": true
        }
        super(UserObject, self).__init__(**object)
