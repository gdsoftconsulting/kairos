null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "TTSQLTOPXT$$1",
            "collections": [
                "TTSQLHS"
            ],
            "userfunctions": [
                "ttcoeff"
            ],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, hashid as label, (totaltime / 1000.0 / deltatime) / ttcoeff as value from TTSQLHS, (select ttcoeff() as ttcoeff) as foo) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": true
        }
        super(UserObject, self).__init__(**object)
