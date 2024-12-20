null=None
true=True
false=False

class UserObject(dict):
    def __init__(s):
        object = {
            "id": "VMSTATCPU",
            "title": "CPU Usage - Run queue",
            "subtitle": "",
            "reftime": "VMSTATREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "CPU usage (%)",
                    "position": "LEFT",
                    "scaling": "LINEAR",
                    "properties": {},
                    "minvalue": 0,
                    "maxvalue": 110,
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
                                            "projection": "'usr'::text",
                                            "restriction": "",
                                            "value": "vms_us"
                                        },
                                        {
                                            "table": "VMSTAT",
                                            "projection": "'sys'::text",
                                            "restriction": "",
                                            "value": "vms_sy"
                                        },
                                        {
                                            "table": "VMSTAT",
                                            "projection": "'usr + sys'::text",
                                            "restriction": "",
                                            "value": "vms_us + vms_sy"
                                        },
                                        {
                                            "table": "VMSTAT",
                                            "projection": "'idle'::text",
                                            "restriction": "",
                                            "value": "vms_id"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Run queue",
                    "position": "RIGHT",
                    "scaling": "LINEAR",
                    "properties": {},
                    "minvalue": 0,
                    "maxvalue": 110,
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
                                            "projection": "'run queue'::text",
                                            "restriction": "",
                                            "value": "vms_r"
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