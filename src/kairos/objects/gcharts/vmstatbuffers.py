null=None
true=True
false=False

class UserObject(dict):
    def __init__(s):
        object = {
            "id": "VMSTATBUFFERS",
            "title": "Buffers in and out",
            "subtitle": "",
            "reftime": "VMSTATREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "Buffers(#)",
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
                                            "projection": "'buffers in'::text",
                                            "restriction": "",
                                            "value": "vms_bi"
                                        },
                                        {
                                            "table": "VMSTAT",
                                            "projection": "'buffers out'::text",
                                            "restriction": "",
                                            "value": "vms_bo"
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