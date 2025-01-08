class UserObject(dict):
    def __init__(s):
        object = {
            "id": "MEMINFOSTAT",
            "title": "Memory usage",
            "subtitle": "",
            "reftime": "MEMINFOREFTIME",
            "type": "chart",
            "yaxis": [
                {
                    "title": "Memory usage (in Gigabytes)",
                    "position": "LEFT",
                    "scaling": "LINEAR",
                    "properties": {},
                    "minvalue": 0,
                    "maxvalue": null,
                    "renderers": [
                        {
                            "type": "WL",
                            "datasets": [
                                {
                                    "query": "MEMINFOSTAT$$1",
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
        super(UserObject, s).__init__(**object)