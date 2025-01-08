null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORARACDBWAITBEI$$1",
            "collections": [
                "DBORARACTTBE"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, event||' / '||inum as label, timewaited as value from DBORARACTTBE where inum::int != 0 and event != 'background cpu time'::text) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": false
        }
        super(UserObject, self).__init__(**object)
