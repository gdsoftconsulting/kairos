null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "NMONLVCPU",
            "title": "Logical vs Virtual percentages",
            "subtitle": "",
            "reftime": "NMONREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "%",
                    "position": "LEFT",
                    "scaling": "LINEAR",
                    "properties": {},
                    "minvalue": 0,
                    "maxvalue": 110,
                    "renderers": [
                        {
                            "type": "L",
                            "datasets": [
                                {
                                    "groupby": "avg",
                                    "projection": "label",
                                    "collections": [
                                        "NMONLPAR"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "(select timestamp, sum(value) as value from NMONLPAR where id in ('VP_User%', 'VP_Sys%', 'VP_Idle%') group by timestamp) as foo",
                                            "projection": "'Virtual usr+sys+idle %'::text",
                                            "restriction": "",
                                            "value": "value"
                                        }
                                    ]
                                },
                                {
                                    "groupby": "avg",
                                    "projection": "label",
                                    "collections": [
                                        "NMONLPAR"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "(select timestamp, sum(value) as value from NMONLPAR where id in ('VP_User%', 'VP_Sys%') group by timestamp) as foo",
                                            "projection": "'Virtual usr+sys %'::text",
                                            "restriction": "",
                                            "value": "value"
                                        }
                                    ]
                                },
                                {
                                    "groupby": "avg",
                                    "projection": "label",
                                    "collections": [
                                        "NMONCPU"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "NMONCPU",
                                            "projection": "'Logical CPU (computation 1) %'::text",
                                            "restriction": "id = 'ALL'",
                                            "value": "usr + sys"
                                        }
                                    ]
                                },
                                {
                                    "groupby": "avg",
                                    "projection": "label",
                                    "collections": [
                                        "NMONCPU"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "(select timestamp, sum(usr + sys) / count(cpus) as value from NMONCPU where id != 'ALL' group by timestamp) as foo",
                                            "projection": "'Logical CPU (computation 2) %'::text",
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
