null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "SARDRWS",
            "title": "Disks - Reads / Writes",
            "subtitle": "",
            "reftime": "SARREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "# of I/Os per second",
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
                                            "value": "rws"
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
                                            "projection": "'Max throughput (all disks)'::text",
                                            "restriction": "",
                                            "value": "rws"
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
