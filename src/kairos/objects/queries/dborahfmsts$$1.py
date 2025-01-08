null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAHFMSTS$$1",
            "collections": [
                "ORAHQS",
                "DBORAMISC"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, 'Application'::text as label, value as value from (select h.timestamp as timestamp, coalesce(apwait_delta,0)::real / 1000000.0 / m.elapsed as value from ORAHQS h, DBORAMISC m where force_matching_signature='%(DBORAHFMSTS)s' and h.timestamp=m.timestamp) as foo) as foo group by timestamp, label order by timestamp",
            "nocache": true,
            "filterable": false
        }
        super(UserObject, self).__init__(**object)
