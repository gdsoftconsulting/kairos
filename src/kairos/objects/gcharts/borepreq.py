null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "BOREPREQ",
            "title": "Business Objects - Top requests for report: %(BOREPREQ)s",
            "subtitle": "",
            "reftime": "BOREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "Average number of concurrent sessions per unit of time",
                    "position": "LEFT",
                    "scaling": "LINEAR",
                    "properties": {
                        "text": {
                            "fill": "red"
                        },
                        "line": {
                            "stroke": "red"
                        }
                    },
                    "minvalue": null,
                    "maxvalue": null,
                    "renderers": [
                        {
                            "type": "SC",
                            "datasets": [
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "BO"
                                    ],
                                    "userfunctions": [
                                        "bocoeff"
                                    ],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "BO, (select bocoeff() as bocoeff) as foo",
                                            "projection": "report||' - '||event_id||' (duration: '||duration||')'::text",
                                            "restriction": "report = '%(BOREPREQ)s'::text",
                                            "value": "executecount * 1.0 / bocoeff"
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
                                        "BO"
                                    ],
                                    "userfunctions": [
                                        "bocoeff"
                                    ],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "BO, (select bocoeff() as bocoeff) as foo",
                                            "projection": "'All requests'::text",
                                            "restriction": "report = '%(BOREPREQ)s'::text",
                                            "value": "executecount * 1.0 / bocoeff"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Estimated response time (in minutes)",
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
                    "minvalue": null,
                    "maxvalue": null,
                    "renderers": [
                        {
                            "type": "L",
                            "datasets": [
                                {
                                    "groupby": "avg",
                                    "projection": "label",
                                    "collections": [
                                        "BO"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "BO",
                                            "projection": "'Response time'::text",
                                            "restriction": "report = '%(BOREPREQ)s'::text",
                                            "value": "duration::real / 60.0"
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
