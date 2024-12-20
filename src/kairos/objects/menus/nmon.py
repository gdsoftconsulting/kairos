class UserObject(dict):
    def __init__(self):
        object = {
            "type": "menu",
            "id": "NMON",
            "tablecondition": "NMONAAA",
            "icon": "fa fa-desktop",
            "label": "NMON",
            "items" : [
                {
                    "type": "submenu",
                    "label": "CPU/LPAR",
                    "items": [
                        { "type": "menuitem", "label": "LPAR CPU overview", "action": "dispchart", "chart": "NMONCPUOV" },
                        { "type": "menuitem", "label": "LPAR CPU utilization vs Entitled capacity", "action": "dispchart", "chart": "NMONCPUE" },
                        { "type": "menuitem", "label": "LPAR CPU utilization vs Virtual capacity", "action": "dispchart", "chart": "NMONCPUV" },
                        { "type": "menuitem", "label": "Logical CPU usage", "action": "dispchart", "chart": "NMONLCPU" },
                        { "type": "menuitem", "label": "Logical CPU idle", "action": "dispchart", "chart": "NMONLCPUIDLE" },
                        { "type": "menuitem", "label": "Logical / Virtual percentages", "action": "dispchart", "chart": "NMONLVCPU" },
                    ]
                },
                {
                    "type": "submenu",
                    "label": "Memory",
                    "items": [
                        { "type": "menuitem", "label": "Memory overview", "action": "dispchart", "chart": "NMONMEMOV" },
                        { "type": "menuitem", "label": "Memory use", "action": "dispchart", "chart": "NMONMEMUSE" },
                    ]
                },
                {
                    "type": "submenu",
                    "label": "Disks",
                    "items": [
                        { "type": "menuitem", "label": "Disks overview", "action": "dispchart", "chart": "NMONDISKOV" },
                        { "type": "menuitem", "label": "Disks read activity", "action": "dispchart", "chart": "NMONDISKRA" },
                        { "type": "menuitem", "label": "Disks write activity", "action": "dispchart", "chart": "NMONDISKWA" },
                        { "type": "menuitem", "label": "Disks busy rate", "action": "dispchart", "chart": "NMONDISKBSY" },
                        { "type": "menuitem", "label": "Disks service time", "action": "dispchart", "chart": "NMONDISKSVC" },
                        { "type": "separator"},
                        { "type": "menuitem", "label": "Choose disk ...", "action": "dispchoice", "choice": "NMONDISK" },
                    ]
                },
                {
                    "type": "submenu",
                    "label": "IO adapters",
                    "items": [
                        { "type": "menuitem", "label": "Read activity", "action": "dispchart", "chart": "NMONIOADAPTRA" },
                        { "type": "menuitem", "label": "Write activity", "action": "dispchart", "chart": "NMONIOADAPTWA" },
                        { "type": "menuitem", "label": "Transfers", "action": "dispchart", "chart": "NMONIOADAPTTF" },
                    ]
                },
                {
                    "type": "submenu",
                    "label": "Network adapters",
                    "items": [
                        { "type": "menuitem", "label": "Read activity", "action": "dispchart", "chart": "NMONNETRA" },
                        { "type": "menuitem", "label": "Write activity", "action": "dispchart", "chart": "NMONNETWA" },
                    ]
                },
                {
                    "type": "submenu",
                    "label": "Asynchronous IOs",
                    "items": [
                        { "type": "menuitem", "label": "Asynchronous IO activity", "action": "dispchart", "chart": "NMONPROCAIO" },
                    ]
                },
                {
                    "type": "submenu",
                    "label": "JFS Filespace",
                    "items": [
                        { "type": "menuitem", "label": "Filespace usage", "action": "dispchart", "chart": "NMONJFSFILE" },
                    ]
                },
                {
                    "type": "submenu",
                    "label": "Paging",
                    "items": [
                        { "type": "menuitem", "label": "Paging activity", "action": "dispchart", "chart": "NMONPAGE" },
                    ]
                },
                {
                    "type": "submenu",
                    "label": "System",
                    "items": [
                        { "type": "menuitem", "label": "All statistics", "action": "dispchart", "chart": "NMONSYS" },
                    ]
                },
                {
                    "type": "submenu",
                    "label": "Top",
                    "items": [
                        { "type": "menuitem", "label": "Top CPU processes", "action": "dispchart", "chart": "NMONTOPCPU" },
                        { "type": "menuitem", "label": "Top CPU commands", "action": "dispchart", "chart": "NMONTOPCPUCMD" },
                        { "type": "menuitem", "label": "Top memory processes", "action": "dispchart", "chart": "NMONTOPMEM" },
                        { "type": "menuitem", "label": "Top memory commands", "action": "dispchart", "chart": "NMONTOPMEMCMD" },
                    ]
                },
            ]
        }
        super(UserObject, self).__init__(**object)
