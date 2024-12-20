null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "PGSYSNETSENTBYTES",
            "title": "Top interfaces - Volume - Sent bytes",
            "subtitle": "",
            "reftime": "PGSYSREFTIME",
            "type": "chart",
            "yaxis": [
                {
                    "title": "Throughput",
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
                                    "query": "PGSYSNETSENTBYTES$$1",
                                    "timestamp": "timestamp",
                                    "label": "label",
                                    "value": "value",
                                    "onclick": {
                                        "variable": "PGSYSINTERFACE",
                                        "chart": "PGSYSCHOOSEINTERFACE",
                                        "action": "dispchart"
                                    }
                                }
                            ]
                        },
                        {
                            "type": "L",
                            "datasets": [
                                {
                                    "query": "PGSYSNETSENTBYTES$$2",
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
