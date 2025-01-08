null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "DBORASYS",
            "title": "System statistics",
            "subtitle": "",
            "reftime": "DBORAREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "# of seconds each second",
                    "position": "LEFT",
                    "scaling": "LINEAR",
                    "properties": {},
                    "renderers": [
                        {
                            "type": "SA",
                            "datasets": [
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "DBORAOSS",
                                        "DBORAMISC"
                                    ],
                                    "userfunctions": [],
                                    "filterable": false,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "(select t.timestamp, statistic, value, avgelapsed from DBORAOSS as t, DBORAMISC as m where t.timestamp=m.timestamp and t.kairos_nodeid=m.kairos_nodeid) as foo",
                                            "projection": "statistic",
                                            "restriction": "statistic in ('USER_TIME','SYS_TIME')",
                                            "value": "value*1.0/100/avgelapsed"
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
                                        "DBORAOSS"
                                    ],
                                    "userfunctions": [],
                                    "filterable": false,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "DBORAOSS",
                                            "projection": "statistic",
                                            "restriction": "statistic='NUM_CPUS'",
                                            "value": "value"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Run Queue / Load",
                    "position": "RIGHT",
                    "scaling": "LINEAR",
                    "properties": {
                        "text": {
                            "fill": "blue"
                        },
                        "line": {
                            "stroke": "blue"
                        }
                    },
                    "renderers": [
                        {
                            "type": "L",
                            "datasets": [
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "DBORAOSS",
                                        "DBORAMISC"
                                    ],
                                    "userfunctions": [],
                                    "filterable": false,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "(select t.timestamp, statistic, value, avgelapsed from DBORAOSS as t, DBORAMISC as m where t.timestamp=m.timestamp and t.kairos_nodeid=m.kairos_nodeid) as foo",
                                            "projection": "statistic",
                                            "restriction": "statistic in ('OS_CPU_WAIT_TIME')",
                                            "value": "value*1.0/100/avgelapsed"
                                        },
                                        {
                                            "table": "(select t.timestamp, statistic, value, avgelapsed from DBORAOSS as t, DBORAMISC as m where t.timestamp=m.timestamp and t.kairos_nodeid=m.kairos_nodeid) as foo",
                                            "projection": "statistic",
                                            "restriction": "statistic in ('LOAD')",
                                            "value": "value"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "IO wait time",
                    "position": "RIGHT",
                    "scaling": "LINEAR",
                    "properties": {
                        "text": {
                            "fill": "green"
                        },
                        "line": {
                            "stroke": "green"
                        }
                    },
                    "renderers": [
                        {
                            "type": "L",
                            "datasets": [
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "DBORAOSS",
                                        "DBORAMISC"
                                    ],
                                    "userfunctions": [],
                                    "filterable": false,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "(select t.timestamp, statistic, value, avgelapsed from DBORAOSS as t, DBORAMISC as m where t.timestamp=m.timestamp and t.kairos_nodeid=m.kairos_nodeid) as foo",
                                            "projection": "statistic",
                                            "restriction": "statistic in ('IOWAIT_TIME')",
                                            "value": "value*1.0/100/avgelapsed"
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
