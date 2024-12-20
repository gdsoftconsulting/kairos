class UserObject(dict):
    def __init__(self):
        object = {
            "type": "menu",
            "id": "SAR",
            "tablecondition": "SARU",
            "icon": "fa fa-desktop",
            "label": "SAR",
            "items" : [
                { "type": "menuitem", "label": "CPU usage - Run queue", "action": "dispchart", "chart": "SARCPU" },
                { "type": "separator"},
                { "type": "menuitem", "label": "IO activity", "action": "dispchart", "chart": "SARIOS" },
                { "type": "separator"},
                {
                    "type": "submenu",
                    "label": "Disks",
                    "items": [
                        { "type": "menuitem", "label": "Disks - Saturation", "action": "dispchart", "chart": "SARDBSY" },
                        { "type": "menuitem", "label": "Disks - Throughput", "action": "dispchart", "chart": "SARDRWS" },
                        { "type": "menuitem", "label": "Disks - Service time", "action": "dispchart", "chart": "SARDSVC" },
                        { "type": "menuitem", "label": "Disks - Wait time", "action": "dispchart", "chart": "SARDWAT" },
                    ]
                },
            ]
        }
        super(UserObject, self).__init__(**object)
