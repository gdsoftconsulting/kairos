null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "DBORAASHOVW",
            "title": "Phasis",
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
                            "type": "WL",
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
                                    "info": {
                                        "variable": "DBORAHELP",
                                        "query": "DBORAHHELP"
                                    },
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "ORAHAS, (select ashcoeff() as ashcoeff) as foo",
                                            "projection": "'IN_HARD_PARSE'::text",
                                            "restriction": "session_type = 'FOREGROUND' and session_state = 'ON CPU' and in_hard_parse = 'Y' and sql_id != ''",
                                            "value": "kairos_count * 1.0 /ashcoeff"
                                        },
                                        {
                                            "table": "ORAHAS, (select ashcoeff() as ashcoeff) as foo",
                                            "projection": "'IN_PARSE'::text",
                                            "restriction": "session_type = 'FOREGROUND' and session_state = 'ON CPU' and in_parse = 'Y' and sql_id != ''",
                                            "value": "kairos_count * 1.0 /ashcoeff"
                                        },
                                        {
                                            "table": "ORAHAS, (select ashcoeff() as ashcoeff) as foo",
                                            "projection": "'IN_SQL_EXECUTION'::text",
                                            "restriction": "session_type = 'FOREGROUND' and session_state = 'ON CPU' and in_sql_execution = 'Y' and sql_id != ''",
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
        super(UserObject, self).__init__(**object)
