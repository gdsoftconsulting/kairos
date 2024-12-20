null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "PGSYSDSKREADBYTES",
            "title": "Top disks - Volume - Reads",
            "subtitle": "",
            "reftime": "PGSYSREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "Throughput",
                    "position": "LEFT",
                    "scaling": "LINEAR",
                    "properties": {},
                    "minvalue": 0,
                    "maxvalue": null,
                    "renderers": [
                        {
                            "type": "SC",
                            "datasets": [
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "vpsutil_disk_io_counters"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": {
                                        "variable": "PGSYSDISK",
                                        "chart": "PGSYSCHOOSEDISK",
                                        "action": "dispchart"
                                    },
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "vpsutil_disk_io_counters",
                                            "projection": "disk",
                                            "restriction": "",
                                            "value": "read_bytes"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "L",
                            "datasets": [
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "vpsutil_disk_io_counters"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": false,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "vpsutil_disk_io_counters",
                                            "projection": "'All disks'::text",
                                            "restriction": "",
                                            "value": "read_bytes"
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
