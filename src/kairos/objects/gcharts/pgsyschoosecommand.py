null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "PGSYSCHOOSECOMMAND",
            "title": "Display metrics for command: %(PGSYSCOMMAND)s",
            "subtitle": "",
            "reftime": "PGSYSREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "CPU Usage",
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
                                        "vpsutil_processes"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": false,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "vpsutil_processes",
                                            "projection": "'USER_TIME'::text",
                                            "restriction": "pname = '%(PGSYSCOMMAND)s'::text",
                                            "value": "usr::real"
                                        },
                                        {
                                            "table": "vpsutil_processes",
                                            "projection": "'SYS_TIME'::text",
                                            "restriction": "pname = '%(PGSYSCOMMAND)s'::text",
                                            "value": "sys::real"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Memory Usage",
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
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "vpsutil_processes"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": false,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "vpsutil_processes",
                                            "projection": "'Resident size'::text",
                                            "restriction": "pname = '%(PGSYSCOMMAND)s'::text",
                                            "value": "rss::real"
                                        },
                                        {
                                            "table": "vpsutil_processes",
                                            "projection": "'Virtual size'::text",
                                            "restriction": "pname = '%(PGSYSCOMMAND)s'::text",
                                            "value": "vms::real"
                                        },
                                        {
                                            "table": "vpsutil_processes",
                                            "projection": "'Text size'::text",
                                            "restriction": "pname = '%(PGSYSCOMMAND)s'::text",
                                            "value": "texts::real"
                                        },
                                        {
                                            "table": "vpsutil_processes",
                                            "projection": "'Shared size'::text",
                                            "restriction": "pname = '%(PGSYSCOMMAND)s'::text",
                                            "value": "shared::real"
                                        },
                                        {
                                            "table": "vpsutil_processes",
                                            "projection": "'Data size'::text",
                                            "restriction": "pname = '%(PGSYSCOMMAND)s'::text",
                                            "value": "datas::real"
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
