null=None
true=True
false=False

class UserObject(dict):
    def __init__(s):
        object = {
            "id": "MEMINFOSTAT",
            "title": "Memory usage",
            "subtitle": "",
            "reftime": "MEMINFOREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "Memory usage (in Gigabytes)",
                    "position": "LEFT",
                    "scaling": "LINEAR",
                    "properties": {},
                    "minvalue": 0,
                    "maxvalue": null,
                    "renderers": [
                        {
                            "type": "WL",
                            "datasets": [
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "MEMINFO"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "MEMINFO",
                                            "projection": "statistic::text",
                                            "restriction": "",
                                            "value": "value/ 1048576"
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