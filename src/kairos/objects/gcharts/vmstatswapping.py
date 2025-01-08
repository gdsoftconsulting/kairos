null=None
true=True
false=False

class UserObject(dict):
    def __init__(s):
        object = {
            "id": "VMSTATSWAPPING",
            "title": "Swapping in and out",
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
                                            "projection": "'swapping in'::text",
                                            "restriction": "",
                                            "value": "vms_si"
                                        },
                                        {
                                            "table": "VMSTAT",
                                            "projection": "'swapping out'::text",
                                            "restriction": "",
                                            "value": "vms_so"
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