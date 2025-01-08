null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "TTSQLTOPX",
            "title": "Top SQL by executions",
            "subtitle": "",
            "reftime": "TTREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "# of executions per second",
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
                                        "TTSQLTOPX"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "TTSQLTOPX",
                                            "projection": "hashid",
                                            "restriction": "",
                                            "value": "execs"
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
