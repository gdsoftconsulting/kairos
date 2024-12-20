class UserObject(dict):
    def __init__(s):
        object = {
            "id": "VMSTATMEMORY",
            "title": "Memory usage",
            "subtitle": "",
            "reftime": "VMSTATREFTIME",
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
                                    "query": "VMSTATMEMORY$$1",
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