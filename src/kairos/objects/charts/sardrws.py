null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "SARDRWS",
            "title": "Disks - Reads / Writes",
            "subtitle": "",
            "reftime": "SARREFTIME",
            "type": "chart",
            "yaxis": [
                {
                    "title": "# of I/Os per second",
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
                                    "query": "SARDRWS$$1",
                                    "timestamp": "timestamp",
                                    "label": "label",
                                    "value": "value"
                                },
                                {
                                    "query": "SARDRWS$$2",
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
