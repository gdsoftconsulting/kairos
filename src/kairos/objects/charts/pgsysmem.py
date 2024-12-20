null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "PGSYSMEM",
            "title": "Memory usage",
            "subtitle": "",
            "reftime": "PGSYSREFTIME",
            "type": "chart",
            "yaxis": [
                {
                    "title": "Size",
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
                                    "query": "PGSYSMEM$$1",
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
