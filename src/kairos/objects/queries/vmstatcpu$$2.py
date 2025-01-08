class UserObject(dict):
    def __init__(s):
        object = {
            "type": "query",
            "id": "VMSTATCPU$$2",
            "collections": [
                "VMSTAT"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, 'run queue'::text as label, vms_r as value from VMSTAT) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": true
        }
        super(UserObject, s).__init__(**object)