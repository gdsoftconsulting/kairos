class UserObject(dict):
    def __init__(self):
        object = {
            "type": "menu",
            "id": "DBORA",
            "tablecondition": "DBORAMISC",
            "icon": "fa fa-database",
            "label": "Oracle Database",
            "items" : [
                {
                    "type": "submenu",
                    "label": "Summary",
                    "tablecondition": "DBORAWEV",
                    "items": [
                        { "type": "menuitem", "tablecondition": "DBORAAWR", "label": "DB CPU & Wait", "action": "dispchart", "chart": "DBORASUM"},
                        { "type": "menuitem", "tablecondition": "DBORASTATSPACK", "label": "DB CPU & Wait", "action": "dispchart", "chart": "DBORASUM1"},
                        { "type": "menuitem", "tablecondition": "DBORAAWR", "label": "DB CPU & Wait Classes", "action": "dispchart", "chart": "DBORASUMWC" },
                        { "type": "menuitem", "tablecondition": "DBORAAWR", "label": "DB CPU & Wait Classes (Percentage)", "action": "dispchart", "chart": "DBORASUMWCP" },
                        { "type": "menuitem", "tablecondition": "DBORAAWR", "label": "DB CPU & Wait Events", "action": "dispchart", "chart": "DBORASUMWE" },
                        { "type": "menuitem", "tablecondition": "DBORAAWR", "label": "DB Time Model", "action": "dispchart", "chart": "DBORASUME" },
                    ]
                },
                { "type": "separator", "tablecondition": "DBORAOSS"},
                { "type": "menuitem", "tablecondition": "DBORAOSS", "label": "System statistics", "action": "dispchart", "chart": "DBORASYS"},
                { "type": "separator", "tablecondition": "DBORAWEV"},
                {
                    "type": "submenu",
                    "tablecondition": "DBORAWEV",
                    "label": "Wait events",
                    "items": [
                        { "type": "menuitem", "tablecondition": "DBORAWEV", "label": "Top wait events", "action": "dispchart", "chart": "DBORAWEV"},
                        { "type": "menuitem", "tablecondition": "DBORAWEV", "label": "Top wait events (Percentage)", "action": "dispchart", "chart": "DBORAWEVP"},
                        { "type": "menuitem", "tablecondition": "DBORAWEB", "label": "Top background wait events", "action": "dispchart", "chart": "DBORAWEB" },
                        { "type": "menuitem", "tablecondition": "DBORAWEV", "label": "Top wait events - Parallel query", "action": "dispchart", "chart": "DBORAWEP" },
                        { "type": "separator"},
                        { "type": "menuitem", "tablecondition": "DBORAWEV", "label": "Choose wait event ...", "action": "dispchoice", "choice": "DBORAWEV" },
                        { "type": "menuitem", "tablecondition": "DBORAWEB", "label": "Choose background wait event ...", "action": "dispchoice", "choice": "DBORAWEB" },
                        { "type": "menuitem", "tablecondition": "DBORAWEH", "label": "Choose wait event, display histogram ...", "action": "dispchoice", "choice": "DBORAWEH" },
                    ]
                },
                { "type": "separator"},
                {
                    "type": "submenu",
                    "tablecondition": "DBORASTA",
                    "label": "Statistics",
                    "items": [
                        { "type": "menuitem", "label": "Logons", "action": "dispchart", "chart": "DBORALOGONS" },
                        { "type": "menuitem", "label": "User & Recursive calls", "action": "dispchart", "chart": "DBORACAL" },
                        { "type": "menuitem", "label": "Transactional activity", "action": "dispchart", "chart": "DBORACOM" },
                        { "type": "menuitem", "label": "SQL activity - Parsing", "action": "dispchart", "chart": "DBORAPRS" },
                        { "type": "menuitem", "label": "CPU usage", "action": "dispchart", "chart": "DBORACPU" },
                        { "type": "separator"},
                        { "type": "menuitem", "label": "Sorts", "action": "dispchart", "chart": "DBORASORT" },
                        { "type": "menuitem", "label": "Read rows", "action": "dispchart", "chart": "DBORAROWS" },
                        { "type": "menuitem", "label": "Table scans", "action": "dispchart", "chart": "DBORASCAN" },
                        { "type": "separator"},
                        { "type": "menuitem", "label": "Logical & physical reads", "action": "dispchart", "chart": "DBORAPHR" },
                        { "type": "menuitem", "label": "Logical & physical writes", "action": "dispchart", "chart": "DBORACHG" },
                        { "type": "menuitem", "label": "Default cache activity - Hit ratio", "action": "dispchart", "chart": "DBORAHITD" },
                        { "type": "menuitem", "label": "Keep cache activity - Hit ratio", "action": "dispchart", "chart": "DBORAHITK" },
                        { "type": "menuitem", "label": "Recycle cache activity - Hit ratio", "action": "dispchart", "chart": "DBORAHITR" },
                        { "type": "menuitem", "label": "IO overall activity", "action": "dispchart", "chart": "DBORAIOA" },
                        { "type": "separator"},
                        { "type": "menuitem", "label": "SQL*Net traffic", "action": "dispchart", "chart": "DBORASQLNET" },
                        { "type": "separator"},
                        { "type": "menuitem", "label": "Choose statistic ...", "action": "dispchoice", "choice": "DBORASTA" },
                    ]
                },
                {
                    "type": "submenu",
                    "label": "Redo activity",
                    "tablecondition": "DBORASTA",
                    "items": [
                        { "type": "menuitem", "label": "General redo activity", "action": "dispchart", "chart": "DBORARDO" },
                        { "type": "menuitem", "label": "Wait & Write time per operation", "action": "dispchart", "chart": "DBORARDOT" },
                        { "type": "menuitem", "label": "Redo writes & size per write", "action": "dispchart", "chart": "DBORARDOW" },
                    ]
                },
                { "type": "separator"},
                {
                    "type": "submenu",
                    "tablecondition": "DBORASTA",
                    "label": "Advisors",
                    "items": [
                        {
                            "type": "submenu",
                            "tablecondition": "DBORABPA",
                            "label": "Buffer Pool Advisor",
                            "items": [
                                { "type": "menuitem", "label": "Choose buffer pool ...", "action": "dispchoice", "choice": "DBORABUFPOOL" },
                            ]
                        },
                        { "type": "menuitem", "tablecondition": "DBORAPMA", "label": "PGA Advisor", "action": "dispchart", "chart": "DBORAPGAA" },
                        { "type": "menuitem", "tablecondition": "DBORASPA", "label": "Shared Pool Advisor", "action": "dispchart", "chart": "DBORASPA" },
                        { "type": "menuitem", "tablecondition": "DBORASGAA", "label": "SGA Target Advisor", "action": "dispchart", "chart": "DBORASGAA" },
                    ]
                },
                { "type": "separator"},
                {
                    "type": "submenu",
                    "tablecondition": "DBORASQE",
                    "label": "SQL requests",
                    "items": [
                        { "type": "submenu", "tablecondition": "DBORAPDB", "label": " Choose PDB ...",
                            "items": [
                                { "type": "menuitem", "tablecondition": "DBORASQE", "label": "Top SQL by Elapsed time", "action": "dispchoice", "choice": "DBORAPDBSQE" },
                                { "type": "menuitem", "tablecondition": "DBORASQC", "label": "Top SQL by CPU time", "action": "dispchoice", "choice": "DBORAPDBSQC" },
                                { "type": "menuitem", "tablecondition": "DBORASQG", "label": "Top SQL by Gets", "action": "dispchoice", "choice": "DBORAPDBSQG" },
                                { "type": "menuitem", "tablecondition": "DBORASQR", "label": "Top SQL by Reads", "action": "dispchoice", "choice": "DBORAPDBSQR" },
                                { "type": "menuitem", "tablecondition": "DBORASQX", "label": "Top SQL by Executions", "action": "dispchoice", "choice": "DBORAPDBSQX" },
                                { "type": "menuitem", "tablecondition": "DBORASQP", "label": "Top SQL by Parse calls", "action": "dispchoice", "choice": "DBORAPDBSQP" },
                                { "type": "menuitem", "tablecondition": "DBORASQM", "label": "Top SQL by Sharable memory", "action": "dispchoice", "choice": "DBORAPDBSQM" },
                                { "type": "menuitem", "tablecondition": "DBORASQV", "label": "Top SQL by Version count", "action": "dispchoice", "choice": "DBORAPDBSQV" },
                                { "type": "menuitem", "tablecondition": "DBORASQW", "label": "Top SQL by Cluster wait time", "action": "dispchoice", "choice": "DBORAPDBSQW" },
                            ]
                        },
                        { "type": "menuitem", "tablecondition": "DBORASQE", "label": "Top SQL by Elapsed time", "action": "dispchart", "chart": "DBORASQE" },
                        { "type": "menuitem", "tablecondition": "DBORASQC", "label": "Top SQL by CPU time", "action": "dispchart", "chart": "DBORASQC" },
                        { "type": "menuitem", "tablecondition": "DBORASQG", "label": "Top SQL by Gets", "action": "dispchart", "chart": "DBORASQG" },
                        { "type": "menuitem", "tablecondition": "DBORASQR", "label": "Top SQL by Reads", "action": "dispchart", "chart": "DBORASQR" },
                        { "type": "menuitem", "tablecondition": "DBORASQX", "label": "Top SQL by Executions", "action": "dispchart", "chart": "DBORASQX" },
                        { "type": "menuitem", "tablecondition": "DBORASQP", "label": "Top SQL by Parse calls", "action": "dispchart", "chart": "DBORASQP" },
                        { "type": "menuitem", "tablecondition": "DBORASQM", "label": "Top SQL by Sharable memory", "action": "dispchart", "chart": "DBORASQM" },
                        { "type": "menuitem", "tablecondition": "DBORASQV", "label": "Top SQL by Version count", "action": "dispchart", "chart": "DBORASQV" },
                        { "type": "menuitem", "tablecondition": "DBORASQW", "label": "Top SQL by Cluster wait time", "action": "dispchart", "chart": "DBORASQW" },
                    ]
                },
                { "type": "separator"},
                {
                    "type": "submenu",
                    "tablecondition": "DBORATBSR",
                    "label": "Tablespaces & Files",
                    "items": [
                        { "type": "menuitem", "label": "Tablespace reads", "action": "dispchart", "chart": "DBORATBSR" },
                        { "type": "menuitem", "label": "Tablespace writes", "action": "dispchart", "chart": "DBORATBSW" },
                        { "type": "menuitem", "label": "Tablespace read times", "action": "dispchart", "chart": "DBORATBSRT" },
                        { "type": "menuitem", "label": "Tablespace buffer busy wait times", "action": "dispchart", "chart": "DBORATBSB" },
                        { "type": "separator"},
                        { "type": "menuitem", "label": "Choose tablespace, read activity ...", "action": "dispchoice", "choice": "DBORATBS" },
                        { "type": "separator"},
                        { "type": "menuitem", "label": "Database file reads", "action": "dispchart", "chart": "DBORAFILR" },
                        { "type": "menuitem", "label": "Database file writes", "action": "dispchart", "chart": "DBORAFILW" },
                        { "type": "menuitem", "label": "Database file read times", "action": "dispchart", "chart": "DBORAFILRT" },
                        { "type": "menuitem", "label": "Database file buffer busy wait times", "action": "dispchart", "chart": "DBORAFILB" },
                        { "type": "separator"},
                        { "type": "menuitem", "label": "Choose database file, read activity ...", "action": "dispchoice", "choice": "DBORAFIL" },
                    ]
                },
                { "type": "separator"},
                {
                    "type": "submenu",
                    "tablecondition": "DBORASGLR",
                    "label": "Segments",
                    "items": [
                        { "type": "menuitem", "tablecondition": "DBORASGLR", "label": "Top segments by logical reads", "action": "dispchart", "chart": "DBORASGLR" },
                        { "type": "menuitem", "tablecondition": "DBORASGPR", "label": "Top segments by physical reads", "action": "dispchart", "chart": "DBORASGPR" },
                        { "type": "menuitem", "tablecondition": "DBORASGPRR", "label": "Top segments by physical read requests", "action": "dispchart", "chart": "DBORASGPRR" },
                        { "type": "menuitem", "tablecondition": "DBORASGUR", "label": "Top segments by unoptimized reads", "action": "dispchart", "chart": "DBORASGUR" },
                        { "type": "menuitem", "tablecondition": "DBORASGOR", "label": "Top segments by optimized reads", "action": "dispchart", "chart": "DBORASGOR" },
                        { "type": "menuitem", "tablecondition": "DBORASGDPR", "label": "Top segments by direct physical reads", "action": "dispchart", "chart": "DBORASGDPR" },
                        { "type": "menuitem", "tablecondition": "DBORASGPW", "label": "Top segments by physical writes", "action": "dispchart", "chart": "DBORASGPW" },
                        { "type": "menuitem", "tablecondition": "DBORASGPWR", "label": "Top segments by physical write requests", "action": "dispchart", "chart": "DBORASGPWR" },
                        { "type": "menuitem", "tablecondition": "DBORASGDPW", "label": "Top segments by direct physical writes", "action": "dispchart", "chart": "DBORASGDPW" },
                        { "type": "menuitem", "tablecondition": "DBORASGTS", "label": "Top segments by table scans", "action": "dispchart", "chart": "DBORASGTS" },
                        { "type": "menuitem", "tablecondition": "DBORASGDBC", "label": "Top segments by DB blocks changes", "action": "dispchart", "chart": "DBORASGDBC" },
                        { "type": "menuitem", "tablecondition": "DBORASGRLW", "label": "Top segments by row lock waits", "action": "dispchart", "chart": "DBORASGRLW" },
                        { "type": "menuitem", "tablecondition": "DBORASGIW", "label": "Top segments by ITL waits", "action": "dispchart", "chart": "DBORASGIW" },
                        { "type": "menuitem", "tablecondition": "DBORASGBBW", "label": "Top segments by buffer busy waits", "action": "dispchart", "chart": "DBORASGBBW" },
                        { "type": "menuitem", "tablecondition": "DBORASGGCBB", "label": "Top segments by global cache buffer busy", "action": "dispchart", "chart": "DBORASGGCBB" },
                        { "type": "menuitem", "tablecondition": "DBORASGCRBR", "label": "Top segments by CR blocks received", "action": "dispchart", "chart": "DBORASGCRBR" },
                        { "type": "menuitem", "tablecondition": "DBORASGCBR", "label": "Top segments by Current blocks received", "action": "dispchart", "chart": "DBORASGCBR" },
                    ]
                },
                { "type": "separator", "tablecondition": "DBORAAWR"},
                {
                    "type": "submenu",
                    "tablecondition": "DBORAAWR",
                    "label": "Services",
                    "items": [
                        { "type": "menuitem", "label": "Services - DB Time", "action": "dispchart", "chart": "DBORASVDBT" },
                        { "type": "menuitem", "label": "Services - DB CPU", "action": "dispchart", "chart": "DBORASVCPU" },
                        { "type": "menuitem", "label": "Services - Logical reads", "action": "dispchart", "chart": "DBORASVLR" },
                        { "type": "menuitem", "label": "Services - Physical reads", "action": "dispchart", "chart": "DBORASVPR" },
                        { "type": "separator"},
                        { "type": "menuitem", "label": "Services - Time waited - User I/O", "action": "dispchart", "chart": "DBORASVUIO" },
                        { "type": "menuitem", "label": "Services - Time waited - Concurrency", "action": "dispchart", "chart": "DBORASVCON" },
                        { "type": "menuitem", "label": "Services - Time waited - Administrative", "action": "dispchart", "chart": "DBORASVADM" },
                        { "type": "menuitem", "label": "Services - Time waited - Network", "action": "dispchart", "chart": "DBORASVNET" },
                        { "type": "separator"},
                        { "type": "menuitem", "label": "Choose service ...", "action": "dispchoice", "choice": "DBORASV" },
                    ]
                },
                { "type": "separator"},
                {
                    "type": "submenu",
                    "tablecondition": "DBORASGA",
                    "label": "SGA usage",
                    "items": [
                        { "type": "menuitem", "label": "SGA usage", "action": "dispchart", "chart": "DBORASGA" },
                        { "type": "menuitem", "label": "Shared Pool usage", "action": "dispchart", "chart": "DBORASGAS" },
                        { "type": "menuitem", "label": "Large Pool usage", "action": "dispchart", "chart": "DBORASGAL" },
                        { "type": "menuitem", "label": "Java Pool usage", "action": "dispchart", "chart": "DBORASGAJ" },
                        { "type": "separator"},
                        { "type": "menuitem", "label": "Choose SGA part ...", "action": "dispchoice", "choice": "DBORASGA" },
                    ]
                },
                { "type": "menuitem", "tablecondition": "DBORAPGA", "label": "PGA usage", "action": "dispchart", "chart": "DBORAPGA" },
                {
                    "type": "submenu",
                    "tablecondition": "DBORALIBR",
                    "label": "Library cache",
                    "items": [
                        { "type": "menuitem", "label": "Reloads", "action": "dispchart", "chart": "DBORALIBR" },
                        { "type": "menuitem", "label": "Invalidations", "action": "dispchart", "chart": "DBORALIBI" },
                    ]
                },
                { "type": "separator", "tablecondition": "ORAHQS"},
                {
                    "type": "submenu",
                    "tablecondition": "ORAHQS",
                    "label": "History",
                    "items" : [
                        {
                            "type": "submenu",
                            "label": "SQL History",
                            "items": [
                                { "type": "menuitem", "label": "Top SQL by Elapsed time", "action": "dispchart", "chart": "DBORAHSQLE" },
                                { "type": "menuitem", "label": "Top SQL by CPU time", "action": "dispchart", "chart": "DBORAHSQLC" },
                                { "type": "menuitem", "label": "Top SQL by Waits - IO", "action": "dispchart", "chart": "DBORAHSQLWI" },
                                { "type": "menuitem", "label": "Top SQL by Waits - Application", "action": "dispchart", "chart": "DBORAHSQLWA" },
                                { "type": "menuitem", "label": "Top SQL by Waits - Concurrency", "action": "dispchart", "chart": "DBORAHSQLWC" },
                                { "type": "menuitem", "label": "Top SQL by Waits - Cluster", "action": "dispchart", "chart": "DBORAHSQLWR" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Choose SQL - Time statistic / sec", "action": "dispchoice", "choice": "DBORAHSQLTS" },
                                { "type": "menuitem", "label": "Choose SQL - Time statistic / exec", "action": "dispchoice", "choice": "DBORAHSQLTX" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Top SQL by Gets", "action": "dispchart", "chart": "DBORAHSQLG" },
                                { "type": "menuitem", "label": "Top SQL by Reads", "action": "dispchart", "chart": "DBORAHSQLR" },
                                { "type": "menuitem", "label": "Top SQL by Executions", "action": "dispchart", "chart": "DBORAHSQLX" },
                                { "type": "menuitem", "label": "Top SQL by Rows processed", "action": "dispchart", "chart": "DBORAHSQLN" },
                                { "type": "menuitem", "label": "Top SQL by Fetches operations", "action": "dispchart", "chart": "DBORAHSQLF" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Choose SQL - Statistics / sec", "action": "dispchoice", "choice": "DBORAHSQLSS" },
                                { "type": "menuitem", "label": "Choose SQL - Statistics / exec", "action": "dispchoice", "choice": "DBORAHSQLSX" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Top SQL by Parse calls", "action": "dispchart", "chart": "DBORAHSQLP" },
                                { "type": "menuitem", "label": "Top SQL by Invalidations", "action": "dispchart", "chart": "DBORAHSQLI" },
                                { "type": "menuitem", "label": "Top SQL by Loads", "action": "dispchart", "chart": "DBORAHSQLL" },
                                { "type": "menuitem", "label": "Top SQL by Sorts", "action": "dispchart", "chart": "DBORAHSQLS" },
                                { "type": "menuitem", "label": "Top SQL by Version count", "action": "dispchart", "chart": "DBORAHSQLV" },
                                { "type": "menuitem", "label": "Top SQL by Sharable memory", "action": "dispchart", "chart": "DBORAHSQLM" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Choose SQL - All statistics / sec", "action": "dispchoice", "choice": "DBORAHSQLAS" },
                                { "type": "menuitem", "label": "Choose SQL - All statistics / exec", "action": "dispchoice", "choice": "DBORAHSQLAX" },
                            ]
                        },
                        {
                            "type": "submenu",
                            "label": "Plan Hash Value History",
                            "items": [
                                { "type": "menuitem", "label": "Top PHV by Elapsed time", "action": "dispchart", "chart": "DBORAHPHVE" },
                                { "type": "menuitem", "label": "Top PHV by CPU time", "action": "dispchart", "chart": "DBORAHPHVC" },
                                { "type": "menuitem", "label": "Top PHV by Waits - IO", "action": "dispchart", "chart": "DBORAHPHVWI" },
                                { "type": "menuitem", "label": "Top PHV by Waits - Application", "action": "dispchart", "chart": "DBORAHPHVWA" },
                                { "type": "menuitem", "label": "Top PHV by Waits - Concurrency", "action": "dispchart", "chart": "DBORAHPHVWC" },
                                { "type": "menuitem", "label": "Top PHV by Waits - Cluster", "action": "dispchart", "chart": "DBORAHPHVWR" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Choose PHV - Time statistic / sec", "action": "dispchoice", "choice": "DBORAHPHVTS" },
                                { "type": "menuitem", "label": "Choose PHV - Time statistic / exec", "action": "dispchoice", "choice": "DBORAHPHVTX" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Top PHV by Gets", "action": "dispchart", "chart": "DBORAHPHVG" },
                                { "type": "menuitem", "label": "Top PHV by Reads", "action": "dispchart", "chart": "DBORAHPHVR" },
                                { "type": "menuitem", "label": "Top PHV by Executions", "action": "dispchart", "chart": "DBORAHPHVX" },
                                { "type": "menuitem", "label": "Top PHV by Rows processed", "action": "dispchart", "chart": "DBORAHPHVN" },
                                { "type": "menuitem", "label": "Top PHV by Fetches operations", "action": "dispchart", "chart": "DBORAHPHVF" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Choose PHV - Statistics / sec", "action": "dispchoice", "choice": "DBORAHPHVSS" },
                                { "type": "menuitem", "label": "Choose PHV - Statistics / exec", "action": "dispchoice", "choice": "DBORAHPHVSX" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Top PHV by Parse calls", "action": "dispchart", "chart": "DBORAHPHVP" },
                                { "type": "menuitem", "label": "Top PHV by Invalidations", "action": "dispchart", "chart": "DBORAHPHVI" },
                                { "type": "menuitem", "label": "Top PHV by Loads", "action": "dispchart", "chart": "DBORAHPHVL" },
                                { "type": "menuitem", "label": "Top PHV by Sorts", "action": "dispchart", "chart": "DBORAHPHVS" },
                                { "type": "menuitem", "label": "Top PHV by Version count", "action": "dispchart", "chart": "DBORAHPHVV" },
                                { "type": "menuitem", "label": "Top PHV by Sharable memory", "action": "dispchart", "chart": "DBORAHPHVM" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Choose PHV - All statistics / sec", "action": "dispchoice", "choice": "DBORAHPHVAS" },
                                { "type": "menuitem", "label": "Choose PHV - All statistics / exec", "action": "dispchoice", "choice": "DBORAHPHVAX" },
                            ]
                        },
                        {
                            "type": "submenu",
                            "label": "Force Matching Signature History",
                            "items": [
                                { "type": "menuitem", "label": "Top FMS by Elapsed time", "action": "dispchart", "chart": "DBORAHFMSE" },
                                { "type": "menuitem", "label": "Top FMS by CPU time", "action": "dispchart", "chart": "DBORAHFMSC" },
                                { "type": "menuitem", "label": "Top FMS by Waits - IO", "action": "dispchart", "chart": "DBORAHFMSWI" },
                                { "type": "menuitem", "label": "Top FMS by Waits - Application", "action": "dispchart", "chart": "DBORAHFMSWA" },
                                { "type": "menuitem", "label": "Top FMS by Waits - Concurrency", "action": "dispchart", "chart": "DBORAHFMSWC" },
                                { "type": "menuitem", "label": "Top FMS by Waits - Cluster", "action": "dispchart", "chart": "DBORAHFMSWR" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Choose FMS - Time statistic / sec", "action": "dispchoice", "choice": "DBORAHFMSTS" },
                                { "type": "menuitem", "label": "Choose FMS - Time statistic / exec", "action": "dispchoice", "choice": "DBORAHFMSTX" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Top FMS by Gets", "action": "dispchart", "chart": "DBORAHFMSG" },
                                { "type": "menuitem", "label": "Top FMS by Reads", "action": "dispchart", "chart": "DBORAHFMSR" },
                                { "type": "menuitem", "label": "Top FMS by Executions", "action": "dispchart", "chart": "DBORAHFMSX" },
                                { "type": "menuitem", "label": "Top FMS by Rows processed", "action": "dispchart", "chart": "DBORAHFMSN" },
                                { "type": "menuitem", "label": "Top FMS by Fetches operations", "action": "dispchart", "chart": "DBORAHFMSF" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Choose FMS - Statistics / sec", "action": "dispchoice", "choice": "DBORAHFMSSS" },
                                { "type": "menuitem", "label": "Choose FMS - Statistics / exec", "action": "dispchoice", "choice": "DBORAHFMSSX" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Top FMS by Parse calls", "action": "dispchart", "chart": "DBORAHFMSP" },
                                { "type": "menuitem", "label": "Top FMS by Invalidations", "action": "dispchart", "chart": "DBORAHFMSI" },
                                { "type": "menuitem", "label": "Top FMS by Loads", "action": "dispchart", "chart": "DBORAHFMSL" },
                                { "type": "menuitem", "label": "Top FMS by Sorts", "action": "dispchart", "chart": "DBORAHFMSS" },
                                { "type": "menuitem", "label": "Top FMS by Version count", "action": "dispchart", "chart": "DBORAHFMSV" },
                                { "type": "menuitem", "label": "Top FMS by Sharable memory", "action": "dispchart", "chart": "DBORAHFMSM" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Choose FMS - All statistics / sec", "action": "dispchoice", "choice": "DBORAHFMSAS" },
                                { "type": "menuitem", "label": "Choose FMS - All statistics / exec", "action": "dispchoice", "choice": "DBORAHFMSAX" },
                            ]
                        },
                    ]
                },
                { "type": "separator", "tablecondition": "ORAHAS"},
                {
                    "type": "submenu",
                    "tablecondition": "ORAHAS",
                    "label": "ASH",
                    "items" : [
                        {
                            "type": "submenu",
                            "label": "DB Time overview",
                            "items": [
                                { "type": "menuitem", "label": "DB Time", "action": "dispchart", "chart": "DBORAASHDBTIME" },
                                { "type": "menuitem", "label": "DB Time model", "action": "dispchart", "chart": "DBORAASHDBTM" },
                                { "type": "menuitem", "label": "Background DB Time", "action": "dispchart", "chart": "DBORAASHBDBTIME" },
                                { "type": "menuitem", "label": "Foreground & Background DB Time", "action": "dispchart", "chart": "DBORAASHOV" },
                            ]
                        },
                        { "type": "separator"},
                        {
                            "type": "submenu",
                            "label": "Wait events",
                            "items": [
                                { "type": "menuitem", "label": "Top foreground wait classes", "action": "dispchart", "chart": "DBORAASHWEC" },
                                { "type": "menuitem", "label": "Top foreground wait events", "action": "dispchart", "chart": "DBORAASHWEV" },
                                { "type": "menuitem", "label": "Top background wait events", "action": "dispchart", "chart": "DBORAASHWEB" },
                                { "type": "separator"},
                                { "type": "submenu", "label": " Choose event ...",
                                    "items": [
                                        { "type": "menuitem", "label": "Top sessions", "action": "dispchoice", "choice": "DBORAASHWEVSES" },
                                        { "type": "menuitem", "label": "Top SQL requests", "action": "dispchoice", "choice": "DBORAASHWEVSQL" },
                                        { "type": "menuitem", "label": "Top SQL operations", "action": "dispchoice", "choice": "DBORAASHWEVOPN" },
                                        { "type": "menuitem", "label": "Top P1 values", "action": "dispchoice", "choice": "DBORAASHWEVP1" },
                                    ]
                                },
                            ]
                        },
                        { "type": "separator"},
                        {
                            "type": "submenu",
                            "label": "Sessions",
                            "items": [
                                { "type": "menuitem", "label": "Top foreground sessions", "action": "dispchart", "chart": "DBORAASHSES" },
                                { "type": "menuitem", "label": "Top blocked foreground sessions", "action": "dispchart", "chart": "DBORAASHBFSES" },
                                { "type": "menuitem", "label": "Top blocking sessions", "action": "dispchart", "chart": "DBORAASHHSES" },
                                { "type": "menuitem", "label": "Top background sessions", "action": "dispchart", "chart": "DBORAASHBSES" },
                                { "type": "menuitem", "label": "PGA allocated - Top sessions", "action": "dispchart", "chart": "DBORAASHPGA" },
                                { "type": "menuitem", "label": "Temp space allocated - Top sessions", "action": "dispchart", "chart": "DBORAASHTMP" },
                                { "type": "separator"},
                                { "type": "submenu", "label": " Choose session ...",
                                    "items": [
                                        { "type": "menuitem", "label": "Top wait events", "action": "dispchoice", "choice": "DBORAASHSESWEV" },
                                        { "type": "menuitem", "label": "Top SQL requests", "action": "dispchoice", "choice": "DBORAASHSESSQL" },
                                        { "type": "menuitem", "label": "Top SQL operations", "action": "dispchoice", "choice": "DBORAASHSESOPN" },
                                        { "type": "menuitem", "label": "PGA allocated", "action": "dispchoice", "choice": "DBORAASHSESPGA" },
                                        { "type": "menuitem", "label": "Temp space allocated", "action": "dispchoice", "choice": "DBORAASHSESTMP" },
                                    ]
                                },
                            ]
                        },
                        { "type": "separator"},
                        {
                            "type": "submenu",
                            "label": "Transactions",
                            "items": [
                                { "type": "menuitem", "label": "Top transactions", "action": "dispchart", "chart": "DBORAASHTX" },
                                { "type": "separator"},
                                { "type": "submenu", "label": " Choose transaction ...",
                                    "items": [
                                        { "type": "menuitem", "label": "Top wait events", "action": "dispchoice", "choice": "DBORAASHTXWEV" },
                                        { "type": "menuitem", "label": "Top SQL requests", "action": "dispchoice", "choice": "DBORAASHTXSQL" },
                                        { "type": "menuitem", "label": "Top SQL operations", "action": "dispchoice", "choice": "DBORAASHTXOPN" },
                                    ]
                                },
                            ]
                        },
                        { "type": "separator"},
                        {
                            "type": "submenu",
                            "label": "SQL requests",
                            "items": [
                                { "type": "menuitem", "label": "Top SQL requests", "action": "dispchart", "chart": "DBORAASHSQL" },
                                { "type": "menuitem", "label": "Top SQL requests on CPU", "action": "dispchart", "chart": "DBORAASHSQLCPU" },
                                { "type": "menuitem", "label": "Top SQL requests in Parsing", "action": "dispchart", "chart": "DBORAASHSQLPRS" },
                                { "type": "menuitem", "label": "Top waiting SQL requests", "action": "dispchart", "chart": "DBORAASHSQLWAIT" },
                                { "type": "menuitem", "label": "Top SQL operations", "action": "dispchart", "chart": "DBORAASHOPN" },
                                { "type": "menuitem", "label": "PGA allocated - Top SQL requests", "action": "dispchart", "chart": "DBORAASHPGA2" },
                                { "type": "menuitem", "label": "Temp space allocated - Top SQL requests", "action": "dispchart", "chart": "DBORAASHTMP2" },
                                { "type": "separator"},
                                { "type": "submenu", "label": "Choose SQL request ...",
                                    "items": [
                                        { "type": "menuitem", "label": "Top wait events", "action": "dispchoice", "choice": "DBORAASHSQLWEV" },
                                        { "type": "menuitem", "label": "Top sessions", "action": "dispchoice", "choice": "DBORAASHSQLSES" },
                                        { "type": "menuitem", "label": "Top sql plan hash values", "action": "dispchoice", "choice": "DBORAASHSQLPHV" },
                                        { "type": "menuitem", "label": "Top execution plan operations", "action": "dispchoice", "choice": "DBORAASHSQLEPO" },
                                        { "type": "menuitem", "label": "Top execute IDs", "action": "dispchoice", "choice": "DBORAASHSQLXID" },
                                        { "type": "menuitem", "label": "Time model", "action": "dispchoice", "choice": "DBORAASHSQLTM" },
                                        { "type": "menuitem", "label": "PGA allocated", "action": "dispchoice", "choice": "DBORAASHSQLPGA" },
                                        { "type": "menuitem", "label": "Temp space allocated", "action": "dispchoice", "choice": "DBORAASHSQLTMP" },
                                    ]
                                },
                            ]
                        },
                        { "type": "separator"},
                        {
                            "type": "submenu",
                            "label": "PDBs",
                            "items": [
                                { "type": "menuitem", "label": "DB Time per PDB", "action": "dispchart", "chart": "DBORAASHPDBDBTIME" },
                                { "type": "separator"},
                                { "type": "submenu", "label": " Choose PDB ...",
                                    "items": [
                                        { "type": "menuitem", "label": "DB Time", "action": "dispchoice", "choice": "DBORAASHPDBDBT" },
                                        { "type": "menuitem", "label": "Top waits events", "action": "dispchoice", "choice": "DBORAASHPDBWEV" },
                                        { "type": "menuitem", "label": "Top sessions", "action": "dispchoice", "choice": "DBORAASHPDBSES" },
                                        { "type": "menuitem", "label": "Top SQL requests", "action": "dispchoice", "choice": "DBORAASHPDBSQL" },
                                        { "type": "menuitem", "label": "Top transactions", "action": "dispchoice", "choice": "DBORAASHPDBTX" },
                                    ]
                                },
                            ]
                        },
                        { "type": "separator"},
                        {
                            "type": "submenu",
                            "label": "Modules",
                            "items": [
                                { "type": "menuitem", "label": " Top modules", "action": "dispchart", "chart": "DBORAASHMOD" },
                                { "type": "separator"},
                                { "type": "submenu", "label": " Choose module ...",
                                    "items": [
                                        { "type": "menuitem", "label": " Top wait events", "action": "dispchoice", "choice": "DBORAASHMODWEV" },
                                        { "type": "menuitem", "label": " Top sessions", "action": "dispchoice", "choice": "DBORAASHMODSES" },
                                        { "type": "menuitem", "label": " Top SQL requests", "action": "dispchoice", "choice": "DBORAASHMODSQL" },
                                    ]
                                },
                            ]
                        },
                        { "type": "separator"},
                        {
                            "type": "submenu",
                            "label": "Programs",
                            "items": [
                                { "type": "menuitem", "label": " Top programs", "action": "dispchart", "chart": "DBORAASHPRG" },
                                { "type": "separator"},
                                { "type": "submenu", "label": " Choose program ...",
                                    "items": [
                                        { "type": "menuitem", "label": " Top wait events", "action": "dispchoice", "choice": "DBORAASHPRGWEV" },
                                        { "type": "menuitem", "label": " Top sessions", "action": "dispchoice", "choice": "DBORAASHPRGSES" },
                                        { "type": "menuitem", "label": " Top SQL requests", "action": "dispchoice", "choice": "DBORAASHPRGSQL" },
                                    ]
                                },
                            ]
                        },
                        { "type": "separator"},
                        {
                            "type": "submenu",
                            "label": "Machines",
                            "items": [
                                { "type": "menuitem", "label": " Top machines", "action": "dispchart", "chart": "DBORAASHMAC" },
                            ]
                        },
                    ]
                },
                { "type": "separator", "tablecondition": "EXACPU"},
                {
                    "type": "submenu",
                    "tablecondition": "EXACPU",
                    "label": "Exadata Cells",
                                "items" : [
                        {
                            "type": "submenu",
                            "label": "Top cells ...",
                            "items": [
                                { "type": "menuitem", "label": "CPU usage", "action": "dispchart", "chart": "EXACPU" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Flash OS IO requests / seconde", "action": "dispchart", "chart": "EXACLLOSIOFR" },
                                { "type": "menuitem", "label": "Flash OS IO megabytes / seconde", "action": "dispchart", "chart": "EXACLLOSIOFV" },
                                { "type": "menuitem", "label": "Flash utilization (%)", "action": "dispchart", "chart": "EXACLLOSIOFU" },
                                { "type": "menuitem", "label": "Flash service time", "action": "dispchart", "chart": "EXACLLOSIOFS" },
                                { "type": "menuitem", "label": "Flash wait time", "action": "dispchart", "chart": "EXACLLOSIOFW" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "Hard disk OS IO requests / seconde", "action": "dispchart", "chart": "EXACLLOSIODR" },
                                { "type": "menuitem", "label": "Hard disk OS IO megabytes / seconde", "action": "dispchart", "chart": "EXACLLOSIODV" },
                                { "type": "menuitem", "label": "Hard disk utilization (%)", "action": "dispchart", "chart": "EXACLLOSIODU" },
                                { "type": "menuitem", "label": "Hard disk service time", "action": "dispchart", "chart": "EXACLLOSIODS" },
                                { "type": "menuitem", "label": "Hard disk wait time", "action": "dispchart", "chart": "EXACLLOSIODW" },
                            ]
                        },
                        { "type": "separator"},
                        {
                            "type": "submenu",
                            "label": "Top databases ...",
                            "items": [
                                { "type": "menuitem", "label": "IO requests on flash / second", "action": "dispchart", "chart": "EXADBIOFR" },
                                { "type": "menuitem", "label": "IO requests on disk / second", "action": "dispchart", "chart": "EXADBIODR" },
                                { "type": "separator"},
                                { "type": "menuitem", "label": "IO throughput on flash / second", "action": "dispchart", "chart": "EXADBIOFV" },
                                { "type": "menuitem", "label": "IO throughput on disk / second", "action": "dispchart", "chart": "EXADBIODV" },
                            ]
                        },
                        { "type": "separator"},
                        {
                            "type": "submenu",
                            "label": "Top hard disks ...",
                            "items": [
                                { "type": "menuitem", "label": "Hard disk OS IO requests / seconde", "action": "dispchart", "chart": "EXADSKOSIODR" },
                                { "type": "menuitem", "label": "Hard disk OS IO megabytes / seconde", "action": "dispchart", "chart": "EXADSKOSIODV" },
                                { "type": "menuitem", "label": "Hard disk utilization (%)", "action": "dispchart", "chart": "EXADSKOSIODU" },
                                { "type": "menuitem", "label": "Hard disk service time", "action": "dispchart", "chart": "EXADSKOSIODS" },
                                { "type": "menuitem", "label": "Hard disk wait time", "action": "dispchart", "chart": "EXADSKOSIODW" },
                            ]
                        },
                        { "type": "separator"},
                        {
                            "type": "submenu",
                            "label": "Top flash devices ...",
                            "items": [
                                { "type": "menuitem", "label": "Flash OS IO requests / seconde", "action": "dispchart", "chart": "EXADSKOSIOFR" },
                                { "type": "menuitem", "label": "Flash OS IO megabytes / seconde", "action": "dispchart", "chart": "EXADSKOSIOFV" },
                                { "type": "menuitem", "label": "Flash utilization (%)", "action": "dispchart", "chart": "EXADSKOSIOFU" },
                                { "type": "menuitem", "label": "Flash service time", "action": "dispchart", "chart": "EXADSKOSIOFS" },
                                { "type": "menuitem", "label": "Flash wait time", "action": "dispchart", "chart": "EXADSKOSIOFW" },
                            ]
                        },
                    ]
                },

            ]
        }
        super(UserObject, self).__init__(**object)
