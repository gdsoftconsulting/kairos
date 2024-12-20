null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORASQLNET$$1",
            "collections": [
                "DBORASTA"
            ],
            "userfunctions": [
                "meet"
            ],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, statistic as label, value / 1024.0 as value from DBORASTA where meet(statistic, '(bytes)')) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": false
        }
        super(UserObject, self).__init__(**object)
