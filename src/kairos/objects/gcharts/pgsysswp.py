null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "PGSYSSWP",
            "title": "Swapping activity",
            "subtitle": "",
            "reftime": "PGSYSREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "Size",
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
                                        "vpsutil_swap_memory"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": false,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "vpsutil_swap_memory",
                                            "projection": "'Total size'::text",
                                            "restriction": "",
                                            "value": "total::real"
                                        },
                                        {
                                            "table": "vpsutil_swap_memory",
                                            "projection": "'Used size'::text",
                                            "restriction": "",
                                            "value": "used::real"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Throughput",
                    "position": "RIGHT",
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
                                        "vpsutil_swap_memory"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": false,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "vpsutil_swap_memory",
                                            "projection": "'Swap in'::text",
                                            "restriction": "",
                                            "value": "sin::real"
                                        },
                                        {
                                            "table": "vpsutil_swap_memory",
                                            "projection": "'Swap out'::text",
                                            "restriction": "",
                                            "value": "sout::real"
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
