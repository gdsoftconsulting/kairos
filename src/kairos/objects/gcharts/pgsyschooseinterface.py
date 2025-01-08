null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "PGSYSCHOOSEINTERFACE",
            "title": "Display metrics for interface: %(PGSYSINTERFACE)s",
            "subtitle": "",
            "reftime": "PGSYSREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "Average volume per operation (packet sent or received)",
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
                                    "groupby": "avg",
                                    "projection": "label",
                                    "collections": [
                                        "vpsutil_net_io_counters"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": false,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "vpsutil_net_io_counters",
                                            "projection": "'Average volume per received packet'::text",
                                            "restriction": "iface = '%(PGSYSINTERFACE)s'::text",
                                            "value": "(case when packets_recv = 0 then 0.0 else bytes_recv / packets_recv end)"
                                        },
                                        {
                                            "table": "vpsutil_net_io_counters",
                                            "projection": "'Average volume per sent packet'::text",
                                            "restriction": "iface = '%(PGSYSINTERFACE)s'::text",
                                            "value": "(case when packets_sent = 0 then 0.0 else bytes_sent / packets_sent end)"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Throughput",
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
                                        "vpsutil_net_io_counters"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": false,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "vpsutil_net_io_counters",
                                            "projection": "'Average received volume per second'::text",
                                            "restriction": "iface = '%(PGSYSINTERFACE)s'::text",
                                            "value": "bytes_recv"
                                        },
                                        {
                                            "table": "vpsutil_net_io_counters",
                                            "projection": "'Average sent volume per second'::text",
                                            "restriction": "iface = '%(PGSYSINTERFACE)s'::text",
                                            "value": "bytes_sent"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Throughput expressed in operations per second",
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
                                        "vpsutil_net_io_counters"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": false,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "vpsutil_net_io_counters",
                                            "projection": "'Average received packets per second'::text",
                                            "restriction": "iface = '%(PGSYSINTERFACE)s'::text",
                                            "value": "packets_recv"
                                        },
                                        {
                                            "table": "vpsutil_net_io_counters",
                                            "projection": "'Average sent packets per second'::text",
                                            "restriction": "iface = '%(PGSYSINTERFACE)s'::text",
                                            "value": "packets_sent"
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
