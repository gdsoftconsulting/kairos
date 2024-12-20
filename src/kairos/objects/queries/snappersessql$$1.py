class UserObject(dict):
    def __init__(s):
        object = {
            "type": "query",
            "id": "SNAPPERSESSQL$$1",
            "collections": [
                "SNAPPER"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, sql_id as label, pthread / 100 as value from SNAPPER where sid||' - '||program = '%(SNAPPERSESSQL)s' and sql_id != '') as foo group by timestamp, label order by timestamp",
            "nocache": true,
            "filterable": true
        }
        super(UserObject, s).__init__(**object)