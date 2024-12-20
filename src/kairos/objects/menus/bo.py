class UserObject(dict):
    def __init__(self):
        object = {
            "type": "menu",
            "id": "BO",
            "tablecondition": "BO",
            "icon": "fa fa-line-chart",
            "label": "Business Objects",
            "items" : [
                {
                    "type": "submenu",
                    "label": "Reports",
                    "items": [
                        { "type": "menuitem", "label": "Top reports", "action": "dispchart", "chart": "BOTOPREP" },
                        { "type": "separator"},
                        { "type": "menuitem", "label": "Choose report, top requests", "action": "dispchoice", "choice": "BOREPREQ" },
                        { "type": "menuitem", "label": "Choose report, top users", "action": "dispchoice", "choice": "BOREPUSR" },
                    ]
                },
                { "type": "separator"},
                {
                    "type": "submenu",
                    "label": "Requests",
                    "items": [
                        { "type": "menuitem", "label": "Top requests", "action": "dispchart", "chart": "BOTOPREQ" },
                    ]
                },
                { "type": "separator"},
                {
                    "type": "submenu",
                    "label": "Users",
                    "items": [
                        { "type": "menuitem", "label": "Top users", "action": "dispchart", "chart": "BOTOPUSR" },
                        { "type": "separator"},
                        { "type": "menuitem", "label": "Choose user, top reports", "action": "dispchoice", "choice": "BOUSRREP" },
                        { "type": "menuitem", "label": "Choose user, top requests", "action": "dispchoice", "choice": "BOUSRREQ" },
                    ]
                },
            ]
        }
        super(UserObject, self).__init__(**object)
