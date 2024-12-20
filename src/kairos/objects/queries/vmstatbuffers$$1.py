class UserObject(dict):
    def __init__(s):
        object = {
            "type": "query",
            "id": "VMSTATBUFFERS$$1",
            "collections": [
                "VMSTAT"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, 'buffers in'::text as label, vms_bi as value from VMSTAT union all select timestamp, 'buffers out'::text as label, vms_bo as value from VMSTAT) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": true
        }
        super(UserObject, s).__init__(**object)