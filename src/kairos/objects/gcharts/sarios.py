null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "SARIOS",
            "title": "I/O activity",
            "subtitle": "",
            "reftime": "SARREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "Number of I/O per second",
                    "position": "LEFT",
                    "scaling": "LINEAR",
                    "properties": {},
                    "minvalue": 0,
                    "maxvalue": null,
                    "renderers": [
                        {
                            "type": "L",
                            "datasets": [
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "SARB"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "SARB",
                                            "projection": "'lwrite'::text",
                                            "restriction": "",
                                            "value": "lwrite"
                                        },
                                        {
                                            "table": "SARB",
                                            "projection": "'lread'::text",
                                            "restriction": "",
                                            "value": "lread"
                                        },
                                        {
                                            "table": "SARB",
                                            "projection": "'pwrite'::text",
                                            "restriction": "",
                                            "value": "pwrite"
                                        },
                                        {
                                            "table": "SARB",
                                            "projection": "'pread'::text",
                                            "restriction": "",
                                            "value": "pread"
                                        },
                                        {
                                            "table": "SARB",
                                            "projection": "'bwrite'::text",
                                            "restriction": "",
                                            "value": "bwrite"
                                        },
                                        {
                                            "table": "SARB",
                                            "projection": "'bread'::text",
                                            "restriction": "",
                                            "value": "bread"
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
