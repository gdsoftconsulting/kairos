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
            "type": "gchart",
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
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "SNAPPER"
                                    ],
                                    "userfunctions": [
                                    ],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "SNAPPER",
                                            "projection": "sid||' - '||program",
                                            "restriction": "program = '%(SNAPPERPRGSES)s'",
                                            "value": "pthread /100"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        super(UserObject, self).__init__(**object)
