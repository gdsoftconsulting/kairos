null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "SNAPPERPRGSES",
            "title": "Top sessions for program: %(SNAPPERPRGSES)s",
            "subtitle": "",
            "reftime": "SNAPPERREFTIME",
            "type": "chart",
            "yaxis": [
                {
                    "title": "Number of active sessions",
                    "position": "LEFT",
                    "scaling": "LINEAR",
                    "properties": {},
                    "minvalue": null,
                    "maxvalue": null,
                    "renderers": [
                        {
                            "type": "SA",
                            "datasets": [
                                {
                                    "query": "SNAPPERPRGSES$$1",
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
