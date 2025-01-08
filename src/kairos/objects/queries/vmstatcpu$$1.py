class UserObject(dict):
    def __init__(s):
        object = {
            "type": "query",
            "id": "VMSTATCPU$$1",
            "collections": [
                "VMSTAT"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, 'usr'::text as label, vms_us as value from VMSTAT union all select timestamp, 'sys'::text as label, vms_sy as value from VMSTAT union all select timestamp, 'usr + sys'::text as label, vms_us + vms_sy as value from VMSTAT union all select timestamp, 'idle'::text as label, vms_id as value from VMSTAT) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": true
        }
        super(UserObject, s).__init__(**object)