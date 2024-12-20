null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "SNAPPERWEVSQL$$1",
            "collections": [
                "SNAPPER"
            ],
            "userfunctions": [
            ],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, sql_id as label, pthread / 100 as value from SNAPPER where event = '%(SNAPPERWEVSQL)s') as foo group by timestamp, label order by timestamp",
            "nocache": true,
            "filterable": true
        }
        super(UserObject, self).__init__(**object)
