null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "id": "DBORARACGCEPD",
            "title": "Global cache efficiency percentages - Disk access",
            "subtitle": "",
            "reftime": "DBORARACREFTIME",
            "type": "gchart",
            "yaxis": [
                {
                    "title": "Disk access (%)",
                    "position": "LEFT",
                    "scaling": "LINEAR",
                    "properties": {
                        "line": {
                            "stroke": "gray"
                        },
                        "text": {
                            "fill": "gray"
                        }
                    },
                    "maxvalue": 110,
                    "renderers": [
                        {
                            "type": "L",
                            "datasets": [
                                {
                                    "groupby": "avg",
                                    "projection": "label",
                                    "collections": [
                                        "DBORARACGCEP"
                                    ],
                                    "userfunctions": [],
                                    "filterable": false,
                                    "nocache": false,
                                    "pieces": [
                                        {
                                            "table": "DBORARACGCEP",
                                            "projection": "inum",
                                            "restriction": "",
                                            "value": "pdisk"
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
