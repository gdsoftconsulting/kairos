null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "PGSYSDSKREADCOUNT",
            "title": "Top disks - Count - Reads",
            "subtitle": "",
            "reftime": "PGSYSREFTIME",
            "type": "chart",
            "yaxis": [
                {
                    "title": "Number of reads / second",
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
                                    "query": "PGSYSDSKREADCOUNT$$1",
                                    "timestamp": "timestamp",
                                    "label": "label",
                                    "value": "value",
                                    "onclick": {
                                        "variable": "PGSYSDISK",
                                        "chart": "PGSYSCHOOSEDISK",
                                        "action": "dispchart"
                                    }
                                }
                            ]
                        },
                        {
                            "type": "L",
                            "datasets": [
                                {
                                    "query": "PGSYSDSKREADCOUNT$$2",
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
