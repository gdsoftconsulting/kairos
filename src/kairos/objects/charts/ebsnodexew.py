null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "EBSNODEXEW",
            "title": "E-Business Suite - Top waiting executions for node: %(EBSNODEXEW)s",
            "subtitle": "",
            "reftime": "EBSREFTIME",
            "type": "chart",
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
                                    "query": "EBSNODEXEW$$1",
                                    "timestamp": "timestamp",
                                    "label": "label",
                                    "value": "value"
                                }
                            ]
                        },
                        {
                            "type": "L",
                            "datasets": [
                                {
                                    "query": "EBSNODEXEW$$2",
                                    "timestamp": "timestamp",
                                    "label": "label",
                                    "value": "value"
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Estimated wait time (in minutes)",
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
                                    "query": "EBSNODEXEW$$3",
                                    "timestamp": "timestamp",
                                    "label": "label",
                                    "value": "value"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        super(UserObject, self).__init__(**object)
