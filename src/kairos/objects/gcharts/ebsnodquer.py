null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "EBSNODQUER",
            "title": "E-Business Suite - Top running queues for node: %(EBSNODQUER)s",
            "subtitle": "",
            "reftime": "EBSREFTIME",
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
                                        "EBS12CM"
                                    ],
                                    "userfunctions": [
                                        "ebscoeff"
                                    ],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "EBS12CM, (select ebscoeff() as ebscoeff) as foo",
                                            "projection": "queue_name",
                                            "restriction": "node_name = '%(EBSNODQUER)s'::text",
                                            "value": "executecount * 1.0 / ebscoeff"
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
                                        "EBS12CM"
                                    ],
                                    "userfunctions": [
                                        "ebscoeff"
                                    ],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "EBS12CM, (select ebscoeff() as ebscoeff) as foo",
                                            "projection": "'Running executions'::text",
                                            "restriction": "node_name = '%(EBSNODQUER)s'::text",
                                            "value": "executecount * 1.0 / ebscoeff"
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
                                        "EBS12CM"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "EBS12CM",
                                            "projection": "'Response time'::text",
                                            "restriction": "node_name = '%(EBSNODQUER)s'::text",
                                            "value": "time * 60.0"
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
