class UserObject(dict):
    def __init__(self):
        object = {
            "type": "menu",
                "id": "MEMINFO",
            "tablecondition": "MEMINFO",
            "icon": "fa fa-desktop",
            "label": "MEMINFO",
            "items" : [
                { "type": "menuitem", "label": "Memory usage", "action": "dispchart", "chart": "MEMINFOSTAT" },
            ]
        }
        super(UserObject, self).__init__(**object)
