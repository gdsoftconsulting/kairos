null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "SARIOS",
            "title": "I/O activity",
            "subtitle": "",
            "reftime": "SARREFTIME",
            "type": "chart",
            "yaxis": [
                {
                    "title": "Number of I/O per second",
                    "position": "LEFT",
                    "scaling": "LINEAR",
                    "properties": {},
                    "minvalue": 0,
                    "maxvalue": null,
                    "renderers": [
                        {
                            "type": "L",
                            "datasets": [
                                {
                                    "query": "SARIOS$$1",
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
