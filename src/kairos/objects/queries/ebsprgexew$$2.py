null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "EBSPRGEXEW$$2",
            "collections": [
                "EBS12CM"
            ],
            "userfunctions": [
                "ebscoeff"
            ],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, 'Waiting executions'::text as label, waitcount * 1.0 / ebscoeff as value from EBS12CM, (select ebscoeff() as ebscoeff) as foo where prg_name = '%(EBSPRGEXEW)s'::text) as foo group by timestamp, label order by timestamp",
            "nocache": true,
            "filterable": true
        }
        super(UserObject, self).__init__(**object)
