null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "SARDSVC",
            "title": "Disks - Service time",
            "subtitle": "",
            "reftime": "SARREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "Service time (ms)",
                    "position": "LEFT",
                    "scaling": "LINEAR",
                    "properties": {},
                    "minvalue": 0,
                    "maxvalue": null,
                    "renderers": [
                        {
                            "type": "L",
                            "datasets": [
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "SARD"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "SARD",
                                            "projection": "device",
                                            "restriction": "",
                                            "value": "avserv"
                                        }
                                    ]
                                },
                                {
                                    "groupby": "max",
                                    "projection": "label",
                                    "collections": [
                                        "SARD"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "SARD",
                                            "projection": "'Max service time (all disks)'::text",
                                            "restriction": "",
                                            "value": "avserv"
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
