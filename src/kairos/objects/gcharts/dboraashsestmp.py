null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "DBORAASHSESTMP",
            "title": "Temp space allocated for session: %(DBORAASHSESTMP)s",
            "subtitle": "",
            "reftime": "DBORAASHREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "Size allocated in bytes",
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
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "ORAHAS",
                                            "projection": "'Temp space allocated'::text",
                                            "restriction": "session_id||' - '||program = '%(DBORAASHSESTMP)s'",
                                            "value": "temp_space_allocated"
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
