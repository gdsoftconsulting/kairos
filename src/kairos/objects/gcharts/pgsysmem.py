null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "PGSYSMEM",
            "title": "Memory usage",
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
                                        "vpsutil_virt_memory"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": false,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "vpsutil_virt_memory",
                                            "projection": "'Total size'::text",
                                            "restriction": "",
                                            "value": "total::real"
                                        },
                                        {
                                            "table": "vpsutil_virt_memory",
                                            "projection": "'Available size'::text",
                                            "restriction": "",
                                            "value": "available::real"
                                        },
                                        {
                                            "table": "vpsutil_virt_memory",
                                            "projection": "'Used size'::text",
                                            "restriction": "",
                                            "value": "used::real"
                                        },
                                        {
                                            "table": "vpsutil_virt_memory",
                                            "projection": "'Free size'::text",
                                            "restriction": "",
                                            "value": "free::real"
                                        },
                                        {
                                            "table": "vpsutil_virt_memory",
                                            "projection": "'Active size'::text",
                                            "restriction": "",
                                            "value": "active::real"
                                        },
                                        {
                                            "table": "vpsutil_virt_memory",
                                            "projection": "'Inactive size'::text",
                                            "restriction": "",
                                            "value": "inactive::real"
                                        },
                                        {
                                            "table": "vpsutil_virt_memory",
                                            "projection": "'Buffers size'::text",
                                            "restriction": "",
                                            "value": "buffers::real"
                                        },
                                        {
                                            "table": "vpsutil_virt_memory",
                                            "projection": "'Cached size'::text",
                                            "restriction": "",
                                            "value": "cached::real"
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
