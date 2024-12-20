class UserObject(dict):
    def __init__(s):
        object = {
            "id": "DBORAASHSQLCPU",
            "title": "Top SQL requests on CPU",
            "subtitle": "",
            "reftime": "DBORAASHREFTIME",
            "type": "chart",
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
                            "type": "WA",
                            "datasets": [
                                {
                                    "query": "DBORAASHSQLCPU$$1",
                                    "timestamp": "timestamp",
                                    "label": "label",
                                    "value": "value",
                                    "info": {
                                        "variable": "DBORAHELP",
                                        "query": "DBORAHHELP"
                                    }
                                }
                            ]
                        },
                        {
                            "type": "WL",
                            "datasets": [
                                {
                                    "query": "DBORAASHSQLCPU$$2",
                                    "timestamp": "timestamp",
                                    "label": "label",
                                    "value": "value"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        super(UserObject, s).__init__(**object)