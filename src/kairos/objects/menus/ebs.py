class UserObject(dict):
    def __init__(self):
        object = {
            "type": "menu",
            "id": "EBS",
            "tablecondition": "EBS12CM",
            "icon": "fa fa-suitcase",
            "label": "E-Business Suite",
            "items" : [
                { "type": "menuitem", "label": "Running & Waiting programs", "action": "dispchart", "chart": "EBSALLPRG" },
                { "type": "menuitem", "label": "Top running executions", "action": "dispchart", "chart": "EBSTOPEXER" },
                { "type": "menuitem", "label": "Top waiting executions", "action": "dispchart", "chart": "EBSTOPEXEW" },
                { "type": "separator"},
                {
                    "type": "submenu",
                    "label": "Programs",
                    "items": [
                        { "type": "menuitem", "label": "Top running programs", "action": "dispchart", "chart": "EBSTOPPRGR" },
                        { "type": "menuitem", "label": "Top waiting programs", "action": "dispchart", "chart": "EBSTOPPRGW" },
                        { "type": "menuitem", "label": "Top programs exited with status E", "action": "dispchart", "chart": "EBSTOPPRGE" },
                        { "type": "menuitem", "label": "Top programs exited with status G", "action": "dispchart", "chart": "EBSTOPPRGG" },
                        { "type": "separator"},
                        {
                            "type": "submenu",
                            "label": "Choose program ...",
                            "items": [
                                { "type": "menuitem", "label": "Top running executions", "action": "dispchoice", "choice": "EBSPRGEXER" },
                                { "type": "menuitem", "label": "Top waiting executions", "action": "dispchoice", "choice": "EBSPRGEXEW" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Show nodes when program was in running state", "action": "dispchoice", "choice": "EBSPRGNODR" },
                                { "type": "menuitem", "label": "Show nodes when program was in waiting state", "action": "dispchoice", "choice": "EBSPRGNODW" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Show queues when program was in running state", "action": "dispchoice", "choice": "EBSPRGQUER" },
                                { "type": "menuitem", "label": "Show queues when program was in waiting state", "action": "dispchoice", "choice": "EBSPRGQUEW" },
                            ]
                        },
                    ]
                },
                { "type": "separator"},
                {
                    "type": "submenu",
                    "label": "Nodes",
                    "items": [
                        { "type": "menuitem", "label": "Running distribution", "action": "dispchart", "chart": "EBSTOPNODR" },
                        { "type": "menuitem", "label": "Waiting distribution", "action": "dispchart", "chart": "EBSTOPNODW" },
                        { "type": "separator"},
                        {
                            "type": "submenu",
                            "label": "Choose node ...",
                            "items": [
                                { "type": "menuitem", "label": "Top running executions", "action": "dispchoice", "choice": "EBSNODEXER" },
                                { "type": "menuitem", "label": "Top waiting executions", "action": "dispchoice", "choice": "EBSNODEXEW" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Show top programs in running state", "action": "dispchoice", "choice": "EBSNODPRGR" },
                                { "type": "menuitem", "label": "Show top programs in waiting state", "action": "dispchoice", "choice": "EBSNODPRGW" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Show queues in running state", "action": "dispchoice", "choice": "EBSNODQUER" },
                                { "type": "menuitem", "label": "Show queues in waiting state", "action": "dispchoice", "choice": "EBSNODQUEW" },
                            ]
                        },
                    ]
                },
                { "type": "separator"},
                {
                    "type": "submenu",
                    "label": "Queues",
                    "items": [
                        { "type": "menuitem", "label": "Running distribution", "action": "dispchart", "chart": "EBSTOPQUER" },
                        { "type": "menuitem", "label": "Waiting distribution", "action": "dispchart", "chart": "EBSTOPQUEW" },
                        { "type": "separator"},
                        {
                            "type": "submenu",
                            "label": "Choose queue ...",
                            "items": [
                                { "type": "menuitem", "label": "Top running executions", "action": "dispchoice", "choice": "EBSQUEEXER" },
                                { "type": "menuitem", "label": "Top waiting executions", "action": "dispchoice", "choice": "EBSQUEEXEW" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Show top programs in running state", "action": "dispchoice", "choice": "EBSQUEPRGR" },
                                { "type": "menuitem", "label": "Show top programs in waiting state", "action": "dispchoice", "choice": "EBSQUEPRGW" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Show nodes in running state", "action": "dispchoice", "choice": "EBSQUENODR" },
                                { "type": "menuitem", "label": "Show nodes in waiting state", "action": "dispchoice", "choice": "EBSQUENODW" },
                            ]
                        },
                    ]
                },
            ]
        }
        super(UserObject, self).__init__(**object)
