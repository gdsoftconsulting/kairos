null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAHPHVAS$$10",
            "collections": [
                "ORAHQS",
                "DBORAMISC"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, 'Fetches'::text as label, value as value from (select h.timestamp as timestamp, coalesce(fetches_delta,0)::real * 1.0 / m.elapsed as value from ORAHQS h, DBORAMISC m where plan_hash_value='%(DBORAHPHVAS)s' and h.timestamp=m.timestamp) as foo) as foo group by timestamp, label order by timestamp",
            "nocache": true,
            "filterable": false
        }
        super(UserObject, self).__init__(**object)
