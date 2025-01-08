null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "SNAPPERPRGWEV",
            "title": "Top wait events for program: %(SNAPPERPRGWEV)s",
            "subtitle": "",
            "reftime": "SNAPPERREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "Number of active sessions",
                    "position": "LEFT",
                    "scaling": "LINEAR",
                    "properties": {},
                    "minvalue": null,
                    "maxvalue": null,
                    "renderers": [
                        {
                            "type": "SA",
                            "datasets": [
                                {
                                    "groupby": "sum",
                                    "projection": "label",
                                    "collections": [
                                        "SNAPPER"
                                    ],
                                    "userfunctions": [
                                    ],
                                    "info": null,
                                    "onclick": null,
                                    "filterable": true,
                                    "nocache": true,
                                    "pieces": [
                                        {
                                            "table": "SNAPPER",
                                            "projection": "case when event is null then 'on cpu' when event is not null then event end",
                                            "restriction": "program = '%(SNAPPERPRGWEV)s'",
                                            "value": "pthread /100"
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
