null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "PGSYSNETSENTBYTES",
            "title": "Top interfaces - Volume - Sent bytes",
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
                                        "vpsutil_net_io_counters"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": {
                                        "variable": "PGSYSINTERFACE",
                                        "chart": "PGSYSCHOOSEINTERFACE",
                                        "action": "dispchart"
                                    },
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "vpsutil_net_io_counters",
                                            "projection": "iface",
                                            "restriction": "",
                                            "value": "bytes_sent"
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
                                        "vpsutil_net_io_counters"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": false,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "vpsutil_net_io_counters",
                                            "projection": "'All interfaces'::text",
                                            "restriction": "",
                                            "value": "bytes_sent"
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
