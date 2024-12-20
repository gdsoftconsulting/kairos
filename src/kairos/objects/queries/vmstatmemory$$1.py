class UserObject(dict):
    def __init__(s):
        object = {
            "type": "query",
            "id": "VMSTATMEMORY$$1",
            "collections": [
                "VMSTAT"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, 'free memory'::text as label, vms_free / 1048576 as value from VMSTAT union all select timestamp, 'virtual memory used'::text as label, vms_swpd / 1048576 as value from VMSTAT union all select timestamp, 'buffers'::text as label, vms_buff / 1048576 as value from VMSTAT union all select timestamp, 'cache'::text as label, vms_cache / 1048576 as value from VMSTAT) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": true
        }
        super(UserObject, s).__init__(**object)