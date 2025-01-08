null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "EBSTOPEXEW",
            "title": "E-Business Suite - Top waiting executions",
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
                                    "query": "EBSTOPEXEW$$1",
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
