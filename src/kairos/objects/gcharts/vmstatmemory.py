null=None
true=True
false=False

class UserObject(dict):
    def __init__(s):
        object = {
            "id": "VMSTATMEMORY",
            "title": "Memory usage",
            "subtitle": "",
            "reftime": "VMSTATREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "Memory usage (in Gigabytes)",
                    "position": "LEFT",
                    "scaling": "LINEAR",
                    "properties": {},
                    "minvalue": 0,
                    "maxvalue": null,
                    "renderers": [
                        {
                            "type": "WL",
                            "datasets": [
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "VMSTAT"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "VMSTAT",
                                            "projection": "'free memory'::text",
                                            "restriction": "",
                                            "value": "vms_free / 1048576"
                                        },
                                        {
                                            "table": "VMSTAT",
                                            "projection": "'virtual memory used'::text",
                                            "restriction": "",
                                            "value": "vms_swpd / 1048576"
                                        },
                                        {
                                            "table": "VMSTAT",
                                            "projection": "'buffers'::text",
                                            "restriction": "",
                                            "value": "vms_buff / 1048576"
                                        },
                                        {
                                            "table": "VMSTAT",
                                            "projection": "'cache'::text",
                                            "restriction": "",
                                            "value": "vms_cache / 1048576"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        super(UserObject, s).__init__(**object)