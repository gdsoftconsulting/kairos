null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "EBSTOPEXER",
            "title": "E-Business Suite - Top running executions",
            "subtitle": "",
            "reftime": "EBSREFTIME",
            "type": "chart",
            "yaxis": [
                {
                    "title": "Average number of programs per unit of time",
                    "position": "LEFT",
                    "scaling": "LINEAR",
                    "properties": {},
                    "minvalue": null,
                    "maxvalue": null,
                    "renderers": [
                        {
                            "type": "SC",
                            "datasets": [
                                {
                                    "query": "EBSTOPEXER$$1",
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
