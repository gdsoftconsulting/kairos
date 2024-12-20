null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "PGDBSCAPPLICATIONS",
            "title": "Database %(PGDBSCAPPLICATIONS)s: Top applications - number of active backends",
            "subtitle": "",
            "reftime": "PGDBSREFTIME",
            "type": "chart",
            "yaxis": [
                {
                    "title": "Number of backends per application",
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
                                    "query": "PGDBSCAPPLICATIONS$$1",
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
