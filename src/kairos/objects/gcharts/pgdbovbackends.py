null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "PGDBOVBACKENDS",
            "title": "Overview - Backends",
            "subtitle": "",
            "reftime": "PGDBREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "Number of backends",
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
                                        "vkpg_stat_database"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "vkpg_stat_database",
                                            "projection": "datname",
                                            "restriction": "",
                                            "value": "numbackends::real"
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
                                        "vkpg_stat_database"
                                    ],
                                    "userfunctions": [],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "vkpg_stat_database",
                                            "projection": "'all databases'::text",
                                            "restriction": "",
                                            "value": "numbackends::real"
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
