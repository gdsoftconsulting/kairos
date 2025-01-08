class UserObject(dict):
    def __init__(s):
        object = {
            "type": "query",
            "id": "VMSTATSWAPPING$$1",
            "collections": [
                "VMSTAT"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, 'swapping in'::text as label, vms_si as value from VMSTAT union all select timestamp, 'swapping out'::text as label, vms_so as value from VMSTAT) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": true
        }
        super(UserObject, s).__init__(**object)