null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "PGDBSCBACKENDS",
            "title": "Database %(PGDBSCBACKENDS)s: Backends",
            "subtitle": "",
            "reftime": "PGDBSREFTIME",
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
                            "type": "L",
                            "datasets": [
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "vkpg_stat_activity"
                                    ],
                                    "userfunctions": [
                                        "pgdbscoeff"
                                    ],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": false,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "vkpg_stat_activity",
                                            "projection": "'Active backends'::text",
                                            "restriction": "datname = '%(PGDBSCBACKENDS)s' and state = 'active' ",
                                            "value": "1.0 / pgdbscoeff(cast(snap_frequency as integer))"
                                        },
                                        {
                                            "table": "vkpg_stat_activity",
                                            "projection": "'All backends'::text",
                                            "restriction": "datname = '%(PGDBSCBACKENDS)s'",
                                            "value": "1.0 / pgdbscoeff(cast(snap_frequency as integer))"
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
