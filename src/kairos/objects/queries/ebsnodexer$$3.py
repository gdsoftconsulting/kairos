null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "EBSNODEXER$$3",
            "collections": [
                "EBS12CM"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, avg(value) as value from (select timestamp, 'Response time'::text as label, time * 60.0 as value from EBS12CM where node_name = '%(EBSNODEXER)s'::text) as foo group by timestamp, label order by timestamp",
            "nocache": true,
            "filterable": true
        }
        super(UserObject, self).__init__(**object)
