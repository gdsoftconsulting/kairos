class UserObject(dict):
    def __init__(self):
        object = {
            "type": "menu",
            "id": "SNAPPER",
            "tablecondition": "SNAPPER",
            "icon": "fa fa-database",
            "label": "Snapper",
            "items" : [
                        { "type": "menuitem", "label": "Average Active Sessions", "action": "dispchart", "chart": "SNAPPERAAS" },
                        { "type": "separator"},
                        {
                            "type": "submenu",
                            "label": "Wait events",
                            "items": [
                                { "type": "menuitem", "label": " Top wait events", "action": "dispchart", "chart": "SNAPPERWEV" },
                                { "type": "separator"},
                                { "type": "submenu", "label": " Choose event ...",
                                    "items": [
                                        { "type": "menuitem", "label": " Top sessions", "action": "dispchoice", "choice": "SNAPPERWEVSES" },
                                        { "type": "menuitem", "label": " Top SQL requests", "action": "dispchoice", "choice": "SNAPPERWEVSQL" },
                                        { "type": "menuitem", "label": " Top object ids", "action": "dispchoice", "choice": "SNAPPERWEVOID" },
                                    ]
                                },
                            ]
                        },
                        { "type": "separator"},
                        {
                            "type": "submenu",
                            "label": "Sessions",
                            "items": [
                                { "type": "menuitem", "label": " Top sessions", "action": "dispchart", "chart": "SNAPPERSES" },
                                { "type": "separator"},
                                { "type": "submenu", "label": " Choose session ...",
                                    "items": [
                                        { "type": "menuitem", "label": " Top wait events", "action": "dispchoice", "choice": "SNAPPERSESWEV" },
                                        { "type": "menuitem", "label": " Top SQL requests", "action": "dispchoice", "choice": "SNAPPERSESSQL" },
                                        { "type": "menuitem", "label": " Top object ids", "action": "dispchoice", "choice": "SNAPPERSESOID" },
                                    ]
                                },
                            ]
                        },
                        { "type": "separator"},
                        {
                            "type": "submenu",
                            "label": "SQL requests",
                            "items": [
                                { "type": "menuitem", "label": " Top SQL requests", "action": "dispchart", "chart": "SNAPPERSQL" },
                                { "type": "menuitem", "label": " Top SQL requests on CPU", "action": "dispchart", "chart": "SNAPPERSQLCPU" },
                                { "type": "menuitem", "label": " Top waiting SQL requests", "action": "dispchart", "chart": "SNAPPERSQLWAIT" },
                                { "type": "separator"},
                                { "type": "submenu", "label": " Choose SQL request ...",
                                    "items": [
                                        { "type": "menuitem", "label": " Top wait events", "action": "dispchoice", "choice": "SNAPPERSQLWEV" },
                                        { "type": "menuitem", "label": " Top sessions", "action": "dispchoice", "choice": "SNAPPERSQLSES" },
                                        { "type": "menuitem", "label": " Top object ids", "action": "dispchoice", "choice": "SNAPPERSQLOID" },
                                    ]
                                },
                            ]
                        },
                        { "type": "separator"},
                        {
                            "type": "submenu",
                            "label": "Schemas",
                            "items": [
                                { "type": "menuitem", "label": " Top schemas", "action": "dispchart", "chart": "SNAPPERSCH" },
                                { "type": "separator"},
                                { "type": "submenu", "label": " Choose schema ...",
                                    "items": [
                                        { "type": "menuitem", "label": " Top wait events", "action": "dispchoice", "choice": "SNAPPERSCHWEV" },
                                        { "type": "menuitem", "label": " Top sessions", "action": "dispchoice", "choice": "SNAPPERSCHSES" },
                                        { "type": "menuitem", "label": " Top SQL requests", "action": "dispchoice", "choice": "SNAPPERSCHSQL" },
                                    ]
                                },
                            ]
                        },
                        { "type": "separator"},
                        {
                            "type": "submenu",
                            "label": "Programs",
                            "items": [
                                { "type": "menuitem", "label": " Top programs", "action": "dispchart", "chart": "SNAPPERPRG" },
                                { "type": "separator"},
                                { "type": "submenu", "label": " Choose program ...",
                                    "items": [
                                        { "type": "menuitem", "label": " Top wait events", "action": "dispchoice", "choice": "SNAPPERPRGWEV" },
                                        { "type": "menuitem", "label": " Top sessions", "action": "dispchoice", "choice": "SNAPPERPRGSES" },
                                        { "type": "menuitem", "label": " Top SQL requests", "action": "dispchoice", "choice": "SNAPPERPRGSQL" },
                                    ]
                                },
                            ]
                        },
                    ]
        }
        super(UserObject, self).__init__(**object)
