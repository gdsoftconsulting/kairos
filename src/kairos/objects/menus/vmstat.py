class UserObject(dict):
    def __init__(self):
        object = {
            "type": "menu",
                "id": "VMSTAT",
            "tablecondition": "VMSTAT",
            "icon": "fa fa-desktop",
            "label": "VMSTAT",
            "items" : [
                { "type": "menuitem", "label": "CPU usage - Run queue", "action": "dispchart", "chart": "VMSTATCPU" },
                { "type": "separator" },
                { "type": "menuitem", "label": "Memory usage", "action": "dispchart", "chart": "VMSTATMEMORY" },
                { "type": "menuitem", "label": "Buffers in and out", "action": "dispchart", "chart": "VMSTATBUFFERS" },
                { "type": "menuitem", "label": "Swapping in and out", "action": "dispchart", "chart": "VMSTATSWAPPING" },
            ]
        }
        super(UserObject, self).__init__(**object)
