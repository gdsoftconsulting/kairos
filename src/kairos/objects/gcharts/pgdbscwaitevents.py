null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "PGDBSCWAITEVENTS",
            "title": "Database %(PGDBSCWAITEVENTS)s: Top wait events",
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
                            "type": "SC",
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
                                    "filterable": true,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "vkpg_stat_activity",
                                            "projection": "wait_event",
                                            "restriction": "datname = '%(PGDBSCWAITEVENTS)s' and state = 'active' ",
                                            "value": "1.0 / pgdbscoeff(cast(snap_frequency as integer))"
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
                                        "vkpg_stat_activity"
                                    ],
                                    "userfunctions": [
                                        "pgdbscoeff"
                                    ],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "vkpg_stat_activity",
                                            "projection": "'All backends'::text",
                                            "restriction": "datname = '%(PGDBSCWAITEVENTS)s'",
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
