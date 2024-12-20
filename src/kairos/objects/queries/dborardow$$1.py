null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORARDOW$$1",
            "collections": [
                "DBORASTA"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, 'redo size / write'::text as label, value as value from (select x.timestamp as timestamp, x.value / y.value as value from DBORASTA x, DBORASTA y where x.statistic = 'redo size' and y.statistic = 'redo writes' and x.timestamp = y.timestamp) as foo) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": false
        }
        super(UserObject, self).__init__(**object)
