null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "PGSYSCPU",
            "title": "CPU usage",
            "subtitle": "",
            "reftime": "PGSYSREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "Seconds per second",
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
                                        "vpsutil_cpu_times"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": false,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "vpsutil_cpu_times",
                                            "projection": "'USER_TIME'::text",
                                            "restriction": "",
                                            "value": "usr"
                                        },
                                        {
                                            "table": "vpsutil_cpu_times",
                                            "projection": "'SYS_TIME'::text",
                                            "restriction": "",
                                            "value": "sys"
                                        },
                                        {
                                            "table": "vpsutil_cpu_times",
                                            "projection": "'IOWAIT_TIME'::text",
                                            "restriction": "",
                                            "value": "iowait"
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
                                        "vpsutil_cpu_times"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": false,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "vpsutil_cpu_times",
                                            "projection": "'NUM_CPUS'::text",
                                            "restriction": "",
                                            "value": "nbcpus"
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
