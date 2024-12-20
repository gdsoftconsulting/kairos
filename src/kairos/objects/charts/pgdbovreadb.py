null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "PGDBOVREADB",
            "title": "Overview - Databases read blocks",
            "subtitle": "",
            "reftime": "PGDBREFTIME",
            "type": "chart",
            "yaxis": [
                {
                    "title": "# of blocks per second",
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
                                    "query": "PGDBOVREADB$$1",
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
                                    "query": "PGDBOVREADB$$2",
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
