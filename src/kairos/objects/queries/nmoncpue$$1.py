null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "NMONCPUE$$1",
            "collections": [
                "NMONLPAR"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, id as label, value as value from NMONLPAR where id in ('EC_User%', 'EC_Sys%', 'EC_Wait%', 'EC_Idle%')) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": true
        }
        super(UserObject, self).__init__(**object)
