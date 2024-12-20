null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "NMONMEMOV$$1",
            "collections": [
                "NMONMEM"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, id as label, value as value from NMONMEM where id in ('memtotal','swaptotal','memfree','Real free(MB)','Real total(MB)','Virtual free(MB)','Virtual total(MB)')) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": true
        }
        super(UserObject, self).__init__(**object)
