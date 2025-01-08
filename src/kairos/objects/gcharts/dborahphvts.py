null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "DBORAHPHVTS",
            "title": "PHV: %(DBORAHPHVTS)s - Statistics per second",
            "subtitle": "",
            "reftime": "DBORAREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "Elapsed (sec) per second",
                    "position": "LEFT",
                    "scaling": "LINEAR",
                    "properties": {},
                    "minvalue": null,
                    "maxvalue": null,
                    "renderers": [
                        {
                            "type": "SA",
                            "datasets": [
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "ORAHQS",
                                        "DBORAMISC"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": false,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "(select h.timestamp as timestamp, coalesce(apwait_delta,0)::real / 1000000.0 / m.elapsed as value from ORAHQS h, DBORAMISC m where plan_hash_value='%(DBORAHPHVTS)s' and h.timestamp=m.timestamp) as foo",
                                            "projection": "'Application'::text",
                                            "restriction": "",
                                            "value": "value"
                                        }
                                    ]
                                },
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "ORAHQS",
                                        "DBORAMISC"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": false,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "(select h.timestamp as timestamp, coalesce(ccwait_delta,0)::real / 1000000.0 / m.elapsed as value from ORAHQS h, DBORAMISC m where plan_hash_value='%(DBORAHPHVTS)s' and h.timestamp=m.timestamp) as foo",
                                            "projection": "'Concurrency'::text",
                                            "restriction": "",
                                            "value": "value"
                                        }
                                    ]
                                },
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "ORAHQS",
                                        "DBORAMISC"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": false,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "(select h.timestamp as timestamp, coalesce(iowait_delta,0)::real / 1000000.0 / m.elapsed as value from ORAHQS h, DBORAMISC m where plan_hash_value='%(DBORAHPHVTS)s' and h.timestamp=m.timestamp) as foo",
                                            "projection": "'User I/O'::text",
                                            "restriction": "",
                                            "value": "value"
                                        }
                                    ]
                                },
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "ORAHQS",
                                        "DBORAMISC"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": false,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "(select h.timestamp as timestamp, coalesce(clwait_delta,0)::real / 1000000.0 / m.elapsed as value from ORAHQS h, DBORAMISC m where plan_hash_value='%(DBORAHPHVTS)s' and h.timestamp=m.timestamp) as foo",
                                            "projection": "'Cluster'::text",
                                            "restriction": "",
                                            "value": "value"
                                        }
                                    ]
                                },
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "ORAHQS",
                                        "DBORAMISC"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": false,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "(select h.timestamp as timestamp, coalesce(cpu_time_delta,0)::real / 1000000.0 / m.elapsed as value from ORAHQS h, DBORAMISC m where plan_hash_value='%(DBORAHPHVTS)s' and h.timestamp=m.timestamp) as foo",
                                            "projection": "'Cpu'::text",
                                            "restriction": "",
                                            "value": "value"
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
                                        "ORAHQS",
                                        "DBORAMISC"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": false,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "(select h.timestamp as timestamp, coalesce(elapsed_time_delta,0)::real / 1000000.0 / m.elapsed as value from ORAHQS h, DBORAMISC m where plan_hash_value='%(DBORAHPHVTS)s' and h.timestamp=m.timestamp) as foo",
                                            "projection": "'Elapsed'::text",
                                            "restriction": "",
                                            "value": "value"
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
