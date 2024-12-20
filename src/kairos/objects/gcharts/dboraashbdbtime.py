null=None
true=True
false=False

class UserObject(dict):
    def __init__(s):
        object = {
            "id": "DBORAASHBDBTIME",
            "title": "DB Time for background sessions",
            "subtitle": "",
            "reftime": "DBORAASHREFTIME",
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
                            "type": "WA",
                            "datasets": [
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "ORAHAS"
                                    ],
                                    "userfunctions": [
                                        "ashcoeff"
                                    ],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "ORAHAS, (select ashcoeff() as ashcoeff) as foo",
                                            "projection": "'DB time'::text",
                                            "restriction": "session_type = 'BACKGROUND'",
                                            "value": "kairos_count * 1.0 /ashcoeff"
                                        }
                                    ]
                                },
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "ORAHAS"
                                    ],
                                    "userfunctions": [
                                        "ashcoeff"
                                    ],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "ORAHAS, (select ashcoeff() as ashcoeff) as foo",
                                            "projection": "'waiting'::text",
                                            "restriction": "session_type = 'BACKGROUND' and session_state = 'WAITING'",
                                            "value": "kairos_count * 1.0 /ashcoeff()"
                                        }
                                    ]
                                },
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "ORAHAS"
                                    ],
                                    "userfunctions": [
                                        "ashcoeff"
                                    ],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "ORAHAS, (select ashcoeff() as ashcoeff) as foo",
                                            "projection": "'on cpu'::text",
                                            "restriction": "session_type = 'BACKGROUND' and session_state = 'ON CPU'",
                                            "value": "kairos_count * 1.0 /ashcoeff"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        super(UserObject, s).__init__(**object)