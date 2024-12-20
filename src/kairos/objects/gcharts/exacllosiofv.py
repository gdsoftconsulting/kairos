null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "EXACLLOSIOFV",
            "title": "Flash OS IO volume - Top cells",
            "subtitle": "",
            "reftime": "DBORAREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "# of megabytes per second",
                    "position": "LEFT",
                    "scaling": "LINEAR",
                    "properties": {},
                    "minvalue": null,
                    "maxvalue": null,
                    "renderers": [
                        {
                            "type": "L",
                            "datasets": [
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "EXATOPCLLOSIO"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "EXATOPCLLOSIO",
                                            "projection": "type || ' - ' || cell",
                                            "restriction": "type like 'F/%'",
                                            "value": "vaverage"
                                        }
                                    ]
                                },
                                {
                                    "groupby": "avg",
                                    "projection": "label",
                                    "collections": [
                                        "EXATOPCLLOSIO"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "EXATOPCLLOSIO",
                                            "projection": "'Flash disk maximum capacity for cell 1.5T'::text",
                                            "restriction": "",
                                            "value": "1372.0::real"
                                        },
                                        {
                                            "table": "EXATOPCLLOSIO",
                                            "projection": "'Flash disk maximum capacity for cell 2.9T'::text",
                                            "restriction": "",
                                            "value": "1372.0::real"
                                        },
                                        {
                                            "table": "EXATOPCLLOSIO",
                                            "projection": "'Flash disk maximum capacity for cell 186G'::text",
                                            "restriction": "",
                                            "value": "5488.0::real"
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
