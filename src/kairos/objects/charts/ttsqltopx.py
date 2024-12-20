null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "TTSQLTOPX",
            "title": "Top SQL by executions",
            "subtitle": "",
            "reftime": "TTREFTIME",
            "type": "chart",
            "yaxis": [
                {
                    "title": "# of executions per second",
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
                                    "query": "TTSQLTOPX$$1",
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
