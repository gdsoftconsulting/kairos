null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAPGA$$5",
            "collections": [
                "DBORAPGC"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, 'One pass execs'::text as label, value as value from (select c.timestamp as timestamp, execs1 * elapsed as value from DBORAPGC c, DBORAMISC m where c.timestamp = m.timestamp) as foo) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": false
        }
        super(UserObject, self).__init__(**object)
