null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "SARCPU$$2",
            "collections": [
                "SARQ"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, avg(value) as value from (select timestamp, 'Run queue'::text as label, runqsz as value from SARQ union all select timestamp, 'Swap queue'::text as label, swpqsz as value from SARQ) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": true
        }
        super(UserObject, self).__init__(**object)
