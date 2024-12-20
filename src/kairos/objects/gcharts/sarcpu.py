null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "SARCPU",
            "title": "CPU Usage - Run / Swap queue",
            "subtitle": "",
            "reftime": "SARREFTIME",
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
                            "type": "SA",
                            "datasets": [
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "SARU"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "SARU",
                                            "projection": "'sys'::text",
                                            "restriction": "cpuid = 'all'",
                                            "value": "sys"
                                        },
                                        {
                                            "table": "SARU",
                                            "projection": "'usr'::text",
                                            "restriction": "cpuid = 'all'",
                                            "value": "usr"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Run / Swap queue size",
                    "position": "RIGHT",
                    "scaling": "LINEAR",
                    "properties": {},
                    "minvalue": 0,
                    "maxvalue": null,
                    "renderers": [
                        {
                            "type": "L",
                            "datasets": [
                                {
                                    "groupby": "avg",
                                    "projection": "label",
                                    "collections": [
                                        "SARQ"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "SARQ",
                                            "projection": "'Run queue'::text",
                                            "restriction": "",
                                            "value": "runqsz"
                                        },
                                        {
                                            "table": "SARQ",
                                            "projection": "'Swap queue'::text",
                                            "restriction": "",
                                            "value": "swpqsz"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        super(UserObject, self).__init__(**object)
