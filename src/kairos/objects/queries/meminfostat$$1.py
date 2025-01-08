class UserObject(dict):
    def __init__(s):
        object = {
            "type": "query",
            "id": "MEMINFOSTAT$$1",
            "collections": [
                "MEMINFO"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, statistic::text as label, value/ 1048576 as value from MEMINFO) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": true
        }
        super(UserObject, s).__init__(**object)