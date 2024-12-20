null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "DBORAASHSQLTM",
            "title": "Time model for SQL request: %(DBORAASHSQLTM)s",
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
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "ORAHAS, (select ashcoeff() as ashcoeff) as foo",
                                            "projection": "'IN_SQL_EXECUTION'::text",
                                            "restriction": "sql_id = '%(DBORAASHSQLTM)s' and IN_SQL_EXECUTION = 'Y'",
                                            "value": "kairos_count * 1.0 /ashcoeff"
                                        },
                                        {
                                            "table": "ORAHAS, (select ashcoeff() as ashcoeff) as foo",
                                            "projection": "'IN_PARSE'::text",
                                            "restriction": "sql_id = '%(DBORAASHSQLTM)s' and IN_PARSE = 'Y'",
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
