null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "SNAPPERAAS",
            "title": "Average active sessions",
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
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "SNAPPER",
                                            "projection": "'on cpu'::text",
                                            "restriction": "event = 'ON CPU'",
                                            "value": "pthread /100"
                                        }
                                    ]
                                },
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
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "SNAPPER",
                                            "projection": "'waiting'::text",
                                            "restriction": "event != 'ON CPU'",
                                            "value": "pthread /100"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "L",
                            "datasets": [
                                {
                                    "groupby": "avg",
                                    "projection": "label",
                                    "collections": [
                                        "SNAPPER"
                                    ],
                                    "userfunctions": [
                                    ],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "SNAPPER",
                                            "projection": "'average active sessions'::text",
                                            "restriction": "",
                                            "value": "aas"
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
