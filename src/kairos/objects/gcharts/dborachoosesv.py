null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "DBORACHOOSESV",
            "title": "Display service: %(DBORASV)s - Average wait",
            "subtitle": "",
            "reftime": "DBORAREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "# of seconds per second",
                    "position": "LEFT",
                    "scaling": "LINEAR",
                    "properties": {},
                    "renderers": [
                        {
                            "type": "SA",
                            "datasets": [
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "DBORASVW"
                                    ],
                                    "userfunctions": [],
                                    "filterable": true,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "DBORASVW",
                                            "projection": "'User I/O wait time'::text",
                                            "restriction": "service = '%(DBORASV)s'",
                                            "value": "uiowaitt"
                                        }
                                    ]
                                },
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "DBORASVW"
                                    ],
                                    "userfunctions": [],
                                    "filterable": true,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "DBORASVW",
                                            "projection": "'Administrative wait time'::text",
                                            "restriction": "service = '%(DBORASV)s'",
                                            "value": "admwaitt"
                                        }
                                    ]
                                },
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "DBORASVW"
                                    ],
                                    "userfunctions": [],
                                    "filterable": true,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "DBORASVW",
                                            "projection": "'Concurrency wait time'::text",
                                            "restriction": "service = '%(DBORASV)s'",
                                            "value": "conwaitt"
                                        }
                                    ]
                                },
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "DBORASVW"
                                    ],
                                    "userfunctions": [],
                                    "filterable": true,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "DBORASVW",
                                            "projection": "'Network wait time'::text",
                                            "restriction": "service = '%(DBORASV)s'",
                                            "value": "netwaitt"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "L",
                            "datasets": [
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "DBORASRV"
                                    ],
                                    "userfunctions": [],
                                    "filterable": false,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "DBORASRV",
                                            "projection": "'DB Wait time'::text",
                                            "restriction": "service = '%(DBORASV)s'",
                                            "value": "dbtime - cpu"
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
