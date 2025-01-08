class UserObject(dict):
    def __init__(self):
        object = {
            "type": "menu",
            "id": "DBORARAC",
            "tablecondition": "DBORARACMISC",
            "icon": "fa fa-database",
            "label": "RAC Database",
            "items" : [
                {
                    "type": "submenu",
                    "label": "Summary",
                    "items": [
                        { "type": "menuitem", "label": "Global CPU & Waits", "action": "dispchart", "chart": "DBORARACSUM"},
                        { "type": "menuitem", "label": "DB Time per instance - Overview", "action": "dispchart", "chart": "DBORARACDBTIME" },
                        { "type": "menuitem", "label": "DB Time per instance - Percentage", "action": "dispchart", "chart": "DBORARACDBTIMEP" },
                        { "type": "menuitem", "label": "DB CPU per instance - Overview", "action": "dispchart", "chart": "DBORARACDBCPU" },
                        { "type": "menuitem", "label": "DB Waits per instance - Overview", "action": "dispchart", "chart": "DBORARACDBWAITS" },
                    ]
                },
                { "type": "separator"},
                {
                    "type": "submenu",
                    "label": "Wait events",
                    "items": [
                        { "type": "menuitem", "label": "Foreground wait events / event", "action": "dispchart", "chart": "DBORARACDBWAITE"},
                        { "type": "menuitem", "label": "Foreground wait events / event / instance", "action": "dispchart", "chart": "DBORARACDBWAITEI"},
                        { "type": "menuitem", "label": "Background wait events / event", "action": "dispchart", "chart": "DBORARACDBWAITBE"},
                        { "type": "menuitem", "label": "Background wait events / event / instance", "action": "dispchart", "chart": "DBORARACDBWAITBEI"},
                        { "type": "separator"},
                        { "type": "menuitem", "label": "Choose foreground event - sum per instance", "action": "dispchoice", "choice": "DBORARACFWES" },
                        { "type": "menuitem", "label": "Choose foreground event - average per instance", "action": "dispchoice", "choice": "DBORARACFWEA" },
                    ]
                },
                { "type": "separator"},
                {
                    "type": "submenu",
                    "label": "Interconnect - exchanges between instances",
                    "items": [
                        { "type": "menuitem", "label": "Current blocks - CR blocks", "action": "dispchart", "chart": "DBORARACGCALL"},
                        { "type": "separator"},
                        { "type": "menuitem", "label": "All blocks - from x", "action": "dispchart", "chart": "DBORARACGCALLFX"},
                        { "type": "menuitem", "label": "All blocks - to y", "action": "dispchart", "chart": "DBORARACGCALLTY"},
                        { "type": "menuitem", "label": "All blocks - from x to y", "action": "dispchart", "chart": "DBORARACGCALLFXTY"},
                        { "type": "separator"},
                        { "type": "menuitem", "label": "Current blocks - from x", "action": "dispchart", "chart": "DBORARACGCCUFX"},
                        { "type": "menuitem", "label": "Current blocks - to y", "action": "dispchart", "chart": "DBORARACGCCUTY"},
                        { "type": "menuitem", "label": "Current blocks - from x to y", "action": "dispchart", "chart": "DBORARACGCCUFXTY"},
                        { "type": "separator"},
                        { "type": "menuitem", "label": "CR blocks - from x", "action": "dispchart", "chart": "DBORARACGCCRFX"},
                        { "type": "menuitem", "label": "CR blocks - to y", "action": "dispchart", "chart": "DBORARACGCCRTY"},
                        { "type": "menuitem", "label": "CR blocks - from x to y", "action": "dispchart", "chart": "DBORARACGCCRFXTY"},
                    ]
                },
                { "type": "separator"},
                {
                    "type": "submenu",
                    "label": "Global cache efficiency percentages",
                    "items": [
                        { "type": "menuitem", "label": "Local access", "action": "dispchart", "chart": "DBORARACGCEPL"},
                        { "type": "menuitem", "label": "Remote access", "action": "dispchart", "chart": "DBORARACGCEPR"},
                        { "type": "menuitem", "label": "Disk access", "action": "dispchart", "chart": "DBORARACGCEPD"},
                    ]
                },
            ]
        }
        super(UserObject, self).__init__(**object)
