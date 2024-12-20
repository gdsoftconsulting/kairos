null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "TTSQLTOPXT",
            "title": "Top SQL by execution time",
            "subtitle": "",
            "reftime": "TTREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "Duration in ms",
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
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "TTSQLHS"
                                    ],
                                    "userfunctions": [
                                        "ttcoeff"
                                    ],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "TTSQLHS, (select ttcoeff() as ttcoeff) as foo",
                                            "projection": "hashid",
                                            "restriction": "",
                                            "value": "(totaltime / 1000.0 / deltatime) / ttcoeff"
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
