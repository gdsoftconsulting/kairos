class UserObject(dict):
    def __init__(s):
        object = {
            "id": "VMSTATSWAPPING",
            "title": "Swapping in and out",
            "subtitle": "",
            "reftime": "VMSTATREFTIME",
            "type": "chart",
            "yaxis": [
                {
                    "title": "Buffers(#)",
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
                                    "query": "VMSTATSWAPPING$$1",
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