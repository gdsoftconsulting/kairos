null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAWEB$$1",
            "collections": [
                "DBORAWEB"
            ],
            "userfunctions": [
                "idlewev",
                "pxwev"
            ],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, event as label, time as value from DBORAWEB where not idlewev(event) and not pxwev(event)) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": true
        }
        super(UserObject, self).__init__(**object)
