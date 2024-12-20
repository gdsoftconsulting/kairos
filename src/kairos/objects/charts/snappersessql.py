null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "SNAPPERSESSQL",
            "title": "Top SQL requests for session: %(SNAPPERSESSQL)s",
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
                                    "query": "SNAPPERSESSQL$$1",
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
