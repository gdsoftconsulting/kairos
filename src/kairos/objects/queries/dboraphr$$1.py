null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAPHR$$1",
            "collections": [
                "DBORASTA"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, statistic as label, value as value from DBORASTA where statistic in ('consistent gets','db block gets','physical reads','consistent gets direct','db block gets direct','physical reads direct','consistent gets from cache','db block gets from cache',',physical reads cache','physical read total IO requests','lob reads','physical reads direct (lob)') ) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": false
        }
        super(UserObject, self).__init__(**object)
