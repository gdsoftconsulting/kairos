null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORARACGCALL$$1",
            "collections": [
                "DBORARACGCTS"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, 'Current blocks'::text as label, cublocks as value from DBORARACGCTS union all select timestamp, 'CR blocks'::text as label, crblocks as value from DBORARACGCTS) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": false
        }
        super(UserObject, self).__init__(**object)
