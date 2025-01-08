import logging, re
logging.trace = lambda m: logging.log(5, m)

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "analyzer",
            "id": "ANALAWRHTML",
            "content": "xml",
            "begin": self.begin,
            "end": self.end,
            "rules": [
                {"action": self.aaction, "regexp": r'', "tag": '(h3|h4|table|tr|th|td)'},
            ],
            "contextrules": [
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdbuf", "scope": "DBORABUF"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdbpa", "scope": "DBORABPA"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdenq", "scope": "DBORAENQ"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdfil", "scope": "DBORAFIL"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdlat", "scope": "DBORALAT"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdlaw", "scope": "DBORALAW"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdlib", "scope": "DBORALIB"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdmdc", "scope": "DBORAMDC"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdmtt", "scope": "DBORAMTT"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdoss", "scope": "DBORAOSS"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdpga", "scope": "DBORAPGA"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdpgb", "scope": "DBORAPGB"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdpgc", "scope": "DBORAPGC"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdreq", "scope": "DBORAREQ"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsga", "scope": "DBORASGA"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsglr", "scope": "DBORASGLR"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsgpr", "scope": "DBORASGPR"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsgprr", "scope": "DBORASGPRR"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsgur", "scope": "DBORASGUR"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsgor", "scope": "DBORASGOR"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsgdpr", "scope": "DBORASGDPR"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsgpw", "scope": "DBORASGPW"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsgpwr", "scope": "DBORASGPWR"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsgdpw", "scope": "DBORASGDPW"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsgts", "scope": "DBORASGTS"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsgdbc", "scope": "DBORASGDBC"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsgrlw", "scope": "DBORASGRLW"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsgiw", "scope": "DBORASGIW"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsgbbw", "scope": "DBORASGBBW"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsggcbb", "scope": "DBORASGGCBB"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsgcrbr", "scope": "DBORASGCRBR"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsgcbr", "scope": "DBORASGCBR"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsqc", "scope": "DBORASQC"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsqe", "scope": "DBORASQE"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsqg", "scope": "DBORASQG"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsqm", "scope": "DBORASQM"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsqp", "scope": "DBORASQP"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsqr", "scope": "DBORASQR"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsqv", "scope": "DBORASQV"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsqw", "scope": "DBORASQW"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsqx", "scope": "DBORASQX"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsrv", "scope": "DBORASRV"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsvw", "scope": "DBORASVW"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdsta", "scope": "DBORASTA"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdtab1"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdtab2"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdtab3"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdtab4"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdtbs", "scope": "DBORATBS"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdtms", "scope": "DBORATMS"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdweb", "scope": "DBORAWEB"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdwec", "scope": "DBORAWEC"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdwev", "scope": "DBORAWEV"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdexacpu", "scope": "EXACPU"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdexatopdbior", "scope": "EXATOPDBIOR"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdexatopdbiov", "scope": "EXATOPDBIOV"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdexatopdskior", "scope": "EXATOPDSKIOR"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdexatopdskiov", "scope": "EXATOPDSKIOV"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdexatopcllosio", "scope": "EXATOPCLLOSIO"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdexatopdskosio", "scope": "EXATOPDSKOSIO"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdexatopcllosiol", "scope": "EXATOPCLLOSIOL"},
                {"action": self.atdget, "regexp": r'', "tag": 'td', "context": "tdexatopdskosiol", "scope": "EXATOPDSKOSIOL"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thbuf", "scope": "DBORABUF"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thbpa", "scope": "DBORABPA"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thenq", "scope": "DBORAENQ"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thfil", "scope": "DBORAFIL"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thlat", "scope": "DBORALAT"},
                {"action": self.athget, "regexp": r'Latch|Time', "tag": 'th', "context": "thlaw", "scope": "DBORALAW"},
                {"action": self.athget, "regexp": r'(Namespace|Requests|Reloads|Invali)', "tag": 'th', "context": "thlib", "scope": "DBORALIB"},
                {"action": self.athget, "regexp": r'', "tag": 'th', "context": "thmtt", "scope": "DBORAMTT"},
                {"action": self.athget, "regexp": r'', "tag": 'th', "context": "thmdc", "scope": "DBORAMDC"},
                {"action": self.athget, "regexp": r'', "tag": 'th', "context": "thoss", "scope": "DBORAOSS"},
                {"action": self.athget, "regexp": r'', "tag": 'th', "context": "thpga", "scope": "DBORAPGA"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thpgb", "scope": "DBORAPGB"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thpgc", "scope": "DBORAPGC"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "threq", "scope": "DBORAREQ"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsga", "scope": "DBORASGA"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsglr", "scope": "DBORASGLR"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsgpr", "scope": "DBORASGPR"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsgprr", "scope": "DBORASGPRR"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsgur", "scope": "DBORASGUR"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsgor", "scope": "DBORASGOR"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsgdpr", "scope": "DBORASGDPR"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsgpw", "scope": "DBORASGPW"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsgpwr", "scope": "DBORASGPWR"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsgdpw", "scope": "DBORASGDPW"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsgts", "scope": "DBORASGTS"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsgdbc", "scope": "DBORASGDBC"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsgrlw", "scope": "DBORASGRLW"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsgiw", "scope": "DBORASGIW"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsgbbw", "scope": "DBORASGBBW"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsggcbb", "scope": "DBORASGGCBB"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsgcrbr", "scope": "DBORASGCRBR"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsgcbr", "scope": "DBORASGCBR"},
                {"action": self.athget, "regexp": r'(.+Time.+|Executions|.+Total|SQL.+|PDB)', "tag": 'th', "context": "thsqc", "scope": "DBORASQC"},
                {"action": self.athget, "regexp": r'(.+Time.+|Executions|.+Total|SQL.+|CPU|PDB)', "tag": 'th', "context": "thsqe", "scope": "DBORASQE"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsqg", "scope": "DBORASQG"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsqm", "scope": "DBORASQM"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsqp", "scope": "DBORASQP"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsqr", "scope": "DBORASQR"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsqv", "scope": "DBORASQV"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsqw", "scope": "DBORASQW"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsqx", "scope": "DBORASQX"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsrv", "scope": "DBORASRV"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsvw", "scope": "DBORASVW"},
                {"action": self.athget, "regexp": r'(Statistic|Total)', "tag": 'th', "context": "thsta", "scope": "DBORASTA"},
                {"action": self.athget, "regexp": r'', "tag": 'th', "context": "thtab1"},
                {"action": self.athget, "regexp": r'', "tag": 'th', "context": "thtab2"},
                {"action": self.athget, "regexp": r'', "tag": 'th', "context": "thtab3"},
                {"action": self.athget, "regexp": r'', "tag": 'th', "context": "thtab4"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thtbs", "scope": "DBORATBS"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thtms", "scope": "DBORATMS"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thexacpu", "scope": "EXACPU"},
                {"action": self.athget, "regexp": r'(Name|DBID|Total|Flash|Disk|Captured)', "tag": 'th', "context": "thexatopdbior", "scope": "EXATOPDBIOR"},
                {"action": self.athget, "regexp": r'(Name|DBID|Total|Flash|Disk|Captured)', "tag": 'th', "context": "thexatopdbiov", "scope": "EXATOPDBIOV"},
                {"action": self.athget, "regexp": r'(Disk|Cell|Total|Average$|Small|Large)', "tag": 'th', "context": "thexatopdskior", "scope": "EXATOPDSKIOR"},
                {"action": self.athget, "regexp": r'(Disk|Cell|Total|Average$|Small|Large)', "tag": 'th', "context": "thexatopdskiov", "scope": "EXATOPDSKIOV"},
                {"action": self.athget, "regexp": r'(Type|Name|Total|Avg)', "tag": 'th', "context": "thexatopcllosio", "scope": "EXATOPCLLOSIO"},
                {"action": self.athget, "regexp": r'(Type|Name|Total|Avg)', "tag": 'th', "context": "thexatopdskosio", "scope": "EXATOPDSKOSIO"},
                {"action": self.athget, "regexp": r'(Type|Name|Service|Wait)', "tag": 'th', "context": "thexatopcllosiol", "scope": "EXATOPCLLOSIOL"},
                {"action": self.athget, "regexp": r'(Type|Name|Service|Wait)', "tag": 'th', "context": "thexatopdskosiol", "scope": "EXATOPDSKOSIOL"},
                {"action": self.athget, "regexp": r'(Event|Waits$|Total Wait Time.+|%Time -outs)', "tag": 'th', "context": "thweb", "scope": "DBORAWEB"},
                {"action": self.athget, "regexp": r'(Wait Class|Waits$|Total Wait Time.+|%Time -outs)', "tag": 'th', "context": "thwec", "scope": "DBORAWEC"},
                {"action": self.athget, "regexp": r'(Event|Waits$|Total Wait Time.+|%Time -outs)', "tag": 'th', "context": "thwev", "scope": "DBORAWEV"}
            ],
            "outcontextrules": [
                {"action": self.genstate('thtab1'), "regexp": r'DB Name.*ReleaseRAC', "tag": 'tr'},
                {"action": self.genstate('thtab2'), "regexp": r'InstanceInst.*Time', "tag": 'tr'},
                {"action": self.genstate('thtab3'), "regexp": r'Container DB Id', "tag": 'tr'},
                {"action": self.genstate('thtab4'), "regexp": r'Snap.*Cursors/Session', "tag": 'tr'},
                {"action": self.genstate('thtms'), "regexp": r'Time Model Statistics', "tag": 'h3', "scope": "DBORATMS"},
                {"action": self.genstate('thoss'), "regexp": r'Operating System Statistics', "tag": 'h3', "scope": "DBORAOSS"},
                {"action": self.genstate('thwec'), "regexp": r'Foreground Wait Class', "tag": 'h3', "scope": "DBORAWEC"},
                {"action": self.genstate('thwev'), "regexp": r'Foreground Wait Events', "tag": 'h3', "scope": "DBORAWEV"},
                {"action": self.genstate('thweb'), "regexp": r'Background Wait Events', "tag": 'h3', "scope": "DBORAWEB"},
                {"action": self.genstate('thsrv'), "regexp": r'Service Statistics', "tag": 'h3', "scope": "DBORASRV"},
                {"action": self.genstate('thsvw'), "regexp": r'Service Wait Class Stats', "tag": 'h3', "scope": "DBORASVW"},
                {"action": self.genstate('thsqe'), "regexp": r'SQL ordered by Elapsed Time', "tag": 'h3', "scope": "DBORASQE"},
                {"action": self.genstate('thsqc'), "regexp": r'SQL ordered by CPU Time', "tag": 'h3', "scope": "DBORASQC"},
                {"action": self.genstate('thsqg'), "regexp": r'SQL ordered by Gets', "tag": 'h3', "scope": "DBORASQG"},
                {"action": self.genstate('thsqr'), "regexp": r'SQL ordered by Reads', "tag": 'h3', "scope": "DBORASQR"},
                {"action": self.genstate('thsqx'), "regexp": r'SQL ordered by Executions', "tag": 'h3', "scope": "DBORASQX"},
                {"action": self.genstate('thsqp'), "regexp": r'SQL ordered by Parse Calls', "tag": 'h3', "scope": "DBORASQP"},
                {"action": self.genstate('thsqm'), "regexp": r'SQL ordered by Sharable Memory', "tag": 'h3', "scope": "DBORASQM"},
                {"action": self.genstate('thsqv'), "regexp": r'SQL ordered by Version Count', "tag": 'h3', "scope": "DBORASQV"},
                {"action": self.genstate('thsqw'), "regexp": r'SQL ordered by Cluster Wait Time', "tag": 'h3', "scope": "DBORASQW"},
                {"action": self.genstate('threq'), "regexp": r'Complete List of SQL Text', "tag": 'h3', "scope": "DBORAREQ"},
                {"action": self.genstate('thsta'), "regexp": r'Instance Activity Stats', "tag": 'h3', "scope": "DBORASTA"},
                {"action": self.genstate('thtbs'), "regexp": r'Tablespace IO Stats', "tag": 'h3', "scope": "DBORATBS"},
                {"action": self.genstate('thfil'), "regexp": r'File IO Stats', "tag": 'h3', "scope": "DBORAFIL"},
                {"action": self.genstate('thbuf'), "regexp": r'Buffer Pool Statistics', "tag": 'h3', "scope": "DBORABUF"},
                {"action": self.genstate('thmdc'), "regexp": r'Memory Dynamic Components', "tag": 'h3', "scope": "DBORAMDC"},
                {"action": self.genstate('thmtt'), "regexp": r'Instance Recovery Stats', "tag": 'h3', "scope": "DBORAMTT"},
                {"action": self.genstate('thbpa'), "regexp": r'Buffer Pool Advisory', "tag": 'h3', "scope": "DBORABPA"},
                {"action": self.genstate('thpgb'), "regexp": r'PGA Aggr Summary', "tag": 'h3', "scope": "DBORAPGB"},
                {"action": self.genstate('thpga'), "regexp": r'PGA Aggr Target Stats', "tag": 'h3', "scope": "DBORAPGA"},
                {"action": self.genstate('thpgc'), "regexp": r'PGA Aggr Target Histogram', "tag": 'h3', "scope": "DBORAPGC"},
                {"action": self.genstate('thenq'), "regexp": r'Enqueue Activity', "tag": 'h3', "scope": "DBORAENQ"},
                {"action": self.genstate('thlaw'), "regexp": r'Latch Activity', "tag": 'h3', "scope": "DBORALAW"},
                {"action": self.genstate('thlat'), "regexp": r'Latch Sleep Breakdown', "tag": 'h3', "scope": "DBORALAT"},
                {"action": self.genstate('thsglr'), "regexp": r'Segments by Logical Reads', "tag": 'h3', "scope": "DBORASGLR"},
                {"action": self.genstate('thsgpr'), "regexp": r'Segments by Physical Reads', "tag": 'h3', "scope": "DBORASGPR"},
                {"action": self.genstate('thsgprr'), "regexp": r'Segments by Physical Read Requests', "tag": 'h3', "scope": "DBORASGPRR"},
                {"action": self.genstate('thsgur'), "regexp": r'Segments by UnOptimized Reads', "tag": 'h3', "scope": "DBORASGUR"},
                {"action": self.genstate('thsgor'), "regexp": r'Segments by Optimized Reads', "tag": 'h3', "scope": "DBORASGOR"},
                {"action": self.genstate('thsgdpr'), "regexp": r'Segments by Direct Physical Reads', "tag": 'h3', "scope": "DBORASGDPR"},
                {"action": self.genstate('thsgpw'), "regexp": r'Segments by Physical Writes', "tag": 'h3', "scope": "DBORASGPW"},
                {"action": self.genstate('thsgpwr'), "regexp": r'Segments by Physical Write Requests', "tag": 'h3', "scope": "DBORASGPWR"},
                {"action": self.genstate('thsgdpw'), "regexp": r'Segments by Direct Physical Writes', "tag": 'h3', "scope": "DBORASGDPW"},
                {"action": self.genstate('thsgts'), "regexp": r'Segments by Table Scans', "tag": 'h3', "scope": "DBORASGTS"},
                {"action": self.genstate('thsgdbc'), "regexp": r'Segments by DB Blocks Changes', "tag": 'h3', "scope": "DBORASGDBC"},
                {"action": self.genstate('thsgrlw'), "regexp": r'Segments by Row Lock Waits', "tag": 'h3', "scope": "DBORASGRLW"},
                {"action": self.genstate('thsgiw'), "regexp": r'Segments by ITL Waits', "tag": 'h3', "scope": "DBORASGIW"},
                {"action": self.genstate('thsgbbw'), "regexp": r'Segments by Buffer Busy Waits', "tag": 'h3', "scope": "DBORASGBBW"},
                {"action": self.genstate('thsggcbb'), "regexp": r'Segments by Global Cache Buffer Busy', "tag": 'h3', "scope": "DBORASGGCBB"},
                {"action": self.genstate('thsgcrbr'), "regexp": r'Segments by CR Blocks Received', "tag": 'h3', "scope": "DBORASGCRBR"},
                {"action": self.genstate('thsgcbr'), "regexp": r'Segments by Current Blocks Received', "tag": 'h3', "scope": "DBORASGCBR"},
                {"action": self.genstate('thlib'), "regexp": r'Library Cache Activity', "tag": 'h3', "scope": "DBORALIB"},
                {"action": self.genstate('thsga'), "regexp": r'SGA breakdown difference', "tag": 'h3', "scope": "DBORASGA"},
                {"action": self.genstate('thexatopcllosio'), "regexp": r'Exadata OS IO Statistics - Top Cells$', "tag": 'h4', "scope": "EXATOPCLLOSIO"},
                {"action": self.genstate('thexatopdskosio'), "regexp": r'Exadata OS IO Statistics - Top Disks$', "tag": 'h4', "scope": "EXATOPDSKOSIO"},
                {"action": self.genstate('thexatopcllosiol'), "regexp": r'Exadata OS IO Latency - Top Cells$', "tag": 'h4', "scope": "EXATOPCLLOSIOL"},
                {"action": self.genstate('thexatopdskosiol'), "regexp": r'Exadata OS IO Latency - Top Disks$', "tag": 'h4', "scope": "EXATOPDSKOSIOL"},
                {"action": self.genstate('thexacpu'), "regexp": r'Exadata OS CPU Statistics - Top Cells', "tag": 'h4', "scope": "EXACPU"},
                {"action": self.genstate('thexatopdskior'), "regexp": r'Exadata Cell Server IOPS - Top Disks$', "tag": 'h4', "scope": "EXATOPDSKIOR"},
                {"action": self.genstate('thexatopdskiov'), "regexp": r'Exadata Cell Server IO MB/s - Top Disks$', "tag": 'h4', "scope": "EXATOPDSKIOV"},
                {"action": self.genstate('thexatopdbior'), "regexp": r'Top Databases by IO Requests$', "tag": 'h4', "scope": "EXATOPDBIOR"},
                {"action": self.genstate('thexatopdbiov'), "regexp": r'Top Databases by IO Throughput$', "tag": 'h4', "scope": "EXATOPDBIOV"},
            ]
        }
        super(UserObject, self).__init__(**object)
    def begin(self, a):
        a.collector = {}
        a.cpt = -1
        a.collected = {}
        a.row = {}
        a.reinit = True
        a.sqlid = {}
        a.month = dict(Jan='01',Feb='02',Fev='02',Mar='03',Apr='04',Avr='04',May='05',Mai='05', Jun='06',Jul='07',Aug='08',Sep='09',Oct='10',Nov='11',Dec='12')
        a.setContext('')
    def end(self, a):
        tof=lambda x: float(x.replace(',','').replace(u'\xa0','0')) if x!=u'' else 0.0
        toc=lambda x: x.replace('&quot;',"'").replace('&lt;',"<").replace('&gt;',">").replace(u'\xa0','')
        logging.trace('All keys found in collected data: ' + str(sorted(a.collected.keys(),reverse=True)))
        for x in sorted(a.collected.keys(),reverse=True):
            logging.trace('Found key in collected data: ' + x)
            if x =='zz9':
                dmisc = dict(timestamp='text', sessions='real', avgelapsed='real', elapsed='int')
                for y in a.collected[x]:
                    when = y['@']
                    what = y['SnapTime']
                    if when == 'End Snap:':
                        year = str('20' + what[7:9])
                        month = a.month[str(what[3:6])]
                        day = str(what[0:2])
                        hour = str(what[10:12])
                        min = str(what[13:15])
                        sec = str(what[16:18])
                        a.date = year + month + day + hour + min + sec + "000"
                        a.sessions = int(tof(y['Sessions']))
                    if when == 'Elapsed:':
                        a.dur = int(tof(what[:-6])*60)
                        if 'DBORAMISC' in a.scope: a.emit('DBORAMISC', dmisc, dict(timestamp=a.date, sessions=a.sessions, avgelapsed=a.dur, elapsed=int(a.dur)))
            if x =='zz8':
                dinfo = dict(timestamp='text', type='text', dname='text', dbid='text', dbuname='text', role='text', edition='text', release='text', rac='text', cdb='text', iname='text', inum='text', startup='text', cdbid='text', cname='text', open='text')
                dinfoinstance = dict()
                for y in a.collected[x]:
                    dinfoinstance['dname'] = y['DBName']
                    dinfoinstance['dbid'] = y['DBId']
                    dinfoinstance['dbuname'] = y['UniqueName'] if 'UniqueName' in y else ''
                    dinfoinstance['role'] = y['Role'] if 'Role' in y else ''
                    dinfoinstance['edition'] = y['Edition'] if 'Edition' in y else ''
                    dinfoinstance['release'] = y['Release']
                    dinfoinstance['rac'] = y['RAC'] if 'RAC' in y else 'NO'
                    dinfoinstance['cdb'] = y['CDB'] if 'CDB' in y else 'NO'
                    dinfoinstance['iname'] = y['Instance'] if 'Instance' in y else ''
                    dinfoinstance['inum'] = y['Instnum'] if 'Instnum' in y else ''
                    dinfoinstance['startup'] = y['StartupTime'] if 'StartupTime' in y else ''
                    dinfoinstance['type'] = 'AWR_12C' if '12.2' in y['Release'] and dinfoinstance['cdb'] == 'YES' else 'AWR_11G'
                    dinfoinstance['cdbid'] = ''
                    dinfoinstance['cname'] = ''
                    dinfoinstance['open'] = ''
                    dinfoinstance['timestamp'] = a.date
                    cdb = True if '12.2' in y['Release']  and dinfoinstance['cdb'] == 'YES' else False
                    if 'DBORAINFO' in a.scope and not cdb: a.emit('DBORAINFO', dinfo, dinfoinstance)
            if x =='zz7':
                for y in a.collected[x]:
                    dinfoinstance['iname'] = y['Instance']
                    dinfoinstance['inum'] = y['InstNum']
                    dinfoinstance['startup'] = y['StartupTime']
            if x =='zz6':
                for y in a.collected[x]:
                    dinfoinstance['cdbid'] = y['ContainerDBId']
                    dinfoinstance['cname'] = y['ContainerName']
                    dinfoinstance['open'] = y['OpenTime']
                    if 'DBORAINFO' in a.scope: a.emit('DBORAINFO', dinfo, dinfoinstance)
            if x == 'Foreground Wait Events':
                d = dict(timestamp='text', event='text', count='real', timeouts='real', time='real')
                stack = []
                for y in a.collected[x]:
                    event = y['Event']
                    count = tof(y['Waits']) / a.dur
                    timeouts = tof(y['%Time-outs']) * count / 100
                    time = tof(y['TotalWaitTime(s)']) / a.dur
                    stack.append(dict(timestamp=a.date, event=event, count=count, timeouts=timeouts, time=time))
                a.emit('DBORAWEV', d, stack)
            if x == 'Background Wait Events':
                d = dict(timestamp='text',event='text',count='real',timeouts='real',time='real')
                stack = []
                for y in a.collected[x]:
                    event = y['Event']
                    count = tof(y['Waits']) / a.dur
                    timeouts = tof(y['%Time-outs']) * count / 100
                    time = tof(y['TotalWaitTime(s)']) / a.dur
                    stack.append(dict(timestamp=a.date, event=event, count=count, timeouts=timeouts, time=time))
                a.emit('DBORAWEB', d, stack)
            if x == 'Foreground Wait Class':
                d = dict(timestamp='text',eclass='text',count='real',timeouts='real',time='real')
                stack = []
                for y in a.collected[x]:
                    eclass = y['WaitClass']
                    count = tof(y['Waits']) / a.dur
                    timeouts = tof(y['%Time-outs']) * count / 100
                    time = tof(y['TotalWaitTime(s)']) / a.dur
                    stack.append(dict(timestamp=a.date, eclass=eclass, count=count, timeouts=timeouts, time=time))
                a.emit('DBORAWEC', d, stack)
            if x in ('Instance Activity Stats','Key Instance Activity Stats','Other Instance Activity Stats','Instance Activity Stats - Thread Activity'):
                d = dict(timestamp='text',statistic='text',value='real')
                stack = []
                for y in a.collected[x]:
                    name = y['Statistic']
                    value = tof(y['Total']) / a.dur
                    stack.append(dict(timestamp=a.date, statistic=name, value=value))
                a.emit('DBORASTA', d, stack)
            if x == 'Memory Dynamic Components':
                d=dict(timestamp='text',component='text',operation='text',size='real',vmin='real',vmax='real',opcount='real')
                stack = []
                for y in a.collected[x]:
                    component = y['Component']
                    size = tof(y['CurrentSize(Mb)'])
                    vmin = tof(y['MinSize(Mb)'])
                    vmax = tof(y['MaxSize(Mb)'])
                    opcount = tof(y['OperCount']) / a.dur
                    operation = y['LastOpTyp/Mod']
                    stack.append(dict(timestamp=a.date, component=component, size=size, vmin=vmin, vmax=vmax, opcount=opcount, operation=operation))
                a.emit('DBORAMDC', d, stack)
            if x == 'Instance Recovery Stats':
                d = dict(timestamp='text', targetmttr='real', estdmttr='real', recovestdios='real', actualredoblks='real', targetredoblks='real', logszredoblks='real', logckpttimeoutredoblks='real', logckptintervalredoblks='real', optlogsz='real', estdracavailtime='real')
                stack = []
                for y in a.collected[x]:
                    when = y['@']
                    if when == 'E':
                        f1 = tof(y['TargtMTTR(s)'])
                        f2 = tof(y['EstdMTTR(s)'])
                        f3 = tof(y['RecoveryEstdIOs'])
                        try: f4 = tof(y['ActualRedoBlks'])
                        except: f4 = tof(y['ActualRedoBlks'])
                        try: f5 = tof(y['TargetRedoBlks'])
                        except: f5 = tof(y['TargetRedoBlks'])
                        try: f6 = tof(y['LogSzRedoBlks'])
                        except: f6 = tof(y['LogFileSizeRedoBlks'])
                        try: f7 = tof(y['LogCkptTimeoutRedoBlks'])
                        except: f7 = tof(y['LogCkpTimeoutRedoBlks'])
                        try: f8 = tof(y['LogCkptIntervalRedoBlks'])
                        except: f8 = tof(y['LogCkptIntervalRedoBlks'])
                        try: f9 = tof(y['OptLogSz(M)'])
                        except: f9 = None
                        try: f10 = tof(y['EstdRACAvailTime'])
                        except: f10 = None
                        stack.append(dict(timestamp=a.date, targetmttr=f1, estdmttr=f2, recovestdios=f3, actualredoblks=f4, targetredoblks=f5, logszredoblks=f6, logckpttimeoutredoblks=f7, logckptintervalredoblks=f8, optlogsz=f9, estdracavailtime=f10))
                a.emit('DBORAMTT', d, stack)
            if x == 'Library Cache Activity':
                d = dict(timestamp='text', item='text', gets='real', pins='real', reloads='real', invalidations='real')
                stack = []
                for y in a.collected[x]:
                    item = y['Namespace']
                    gets = tof(y['GetRequests']) / a.dur
                    pins = tof(y['PinRequests']) / a.dur
                    reloads = tof(y['Reloads']) / a.dur
                    invalidations = tof(y['Invali-dations']) / a.dur
                    stack.append(dict(timestamp=a.date, item=item, gets=gets, pins=pins, reloads=reloads, invalidations=invalidations))
                a.emit('DBORALIB', d, stack)
            if x == 'SQL ordered by Elapsed Time':
                d = dict(timestamp='text', sqlid='text', reads='real', execs='real', cpu='real', elapsed='real', percent='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    elapsed = tof(y['ElapsedTime(s)']) / a.dur
                    try: cpu = (tof(y['%CPU']) * elapsed) / 100
                    except: cpu = tof(y['CPUTime(s)'])
                    execs = tof(y['Executions']) / a.dur
                    try: percent = tof(y['%Total'])
                    except: percent = tof(y['%TotalDBTime'])
                    sqlid = y['SQLId']
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    a.sqlid[sqlid] = y['SQLModule']
                    reads=0.0
                    stack.append(dict(timestamp=a.date, sqlid=sqlid, reads=reads, execs=execs, cpu=cpu, elapsed=elapsed, percent=percent, pdb=pdb))
                a.emit('DBORASQE', d, stack)
            if x == 'SQL ordered by Parse Calls':
                d = dict(timestamp='text', sqlid='text', parses='real', execs='real', percent='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    parses = tof(y['ParseCalls']) / a.dur
                    execs = tof(y['Executions']) / a.dur
                    percent = tof(y['%TotalParses'])
                    sqlid = y['SQLId']
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    a.sqlid[sqlid] = y['SQLModule']
                    stack.append(dict(timestamp=a.date, sqlid=sqlid, parses=parses, execs=execs, percent=percent, pdb=pdb))
                a.emit('DBORASQP', d, stack)
            if x == 'SQL ordered by Sharable Memory':
                d = dict(timestamp='text', sqlid='text', sharedmem='real', execs='real', percent='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    sharedmem = tof(y['SharableMem(b)'])
                    execs = tof(y['Executions']) / a.dur
                    percent = tof(y['%Total'])
                    sqlid = y['SQLId']
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    a.sqlid[sqlid] = y['SQLModule']
                    stack.append(dict(timestamp=a.date, sqlid=sqlid, sharedmem=sharedmem, execs=execs, percent=percent, pdb=pdb))
                a.emit('DBORASQM', d, stack)
            if x == 'SQL ordered by Version Count':
                d = dict(timestamp='text', sqlid='text', versioncount='real', execs='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    versioncount = tof(y['VersionCount'])
                    execs = tof(y['Executions']) / a.dur
                    sqlid = y['SQLId']
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    a.sqlid[sqlid] = y['SQLModule']
                    stack.append(dict(timestamp=a.date, sqlid=sqlid, versioncount=versioncount, execs=execs, pdb=pdb))
                a.emit('DBORASQV', d, stack)
            if x == 'SQL ordered by Cluster Wait Time':
                d = dict(timestamp='text', sqlid='text', clusterwait='real', elapsed='real', cpu='real', execs='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    execs = tof(y['Executions']) / a.dur
                    clusterwait = tof(y['ClusterWaitTime(s)']) / a.dur
                    elapsed = tof(y['ElapsedTime(s)']) / a.dur
                    try: cpu = tof(y['%CPU']) * elapsed / 100
                    except: cpu = tof(y['CPUTime(s)'])
                    sqlid = y['SQLId']
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    a.sqlid[sqlid] = y['SQLModule']
                    stack.append(dict(timestamp=a.date, sqlid=sqlid, clusterwait=clusterwait, elapsed=elapsed, cpu=cpu, execs=execs, pdb=pdb))
                a.emit('DBORASQW', d, stack)
            if x == 'SQL ordered by Gets':
                d = dict(timestamp='text', sqlid='text', gets='real', execs='real', percent='real', cpu='real', elapsed='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    gets = tof(y['BufferGets']) / a.dur
                    execs = tof(y['Executions']) / a.dur
                    percent = tof(y['%Total'])
                    elapsed = tof(y['ElapsedTime(s)']) / a.dur
                    try: cpu = tof(y['%CPU']) * elapsed / 100
                    except: cpu = tof(y['CPUTime(s)'])
                    sqlid = y['SQLId']
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    a.sqlid[sqlid] = y['SQLModule']
                    stack.append(dict(timestamp=a.date, sqlid=sqlid, gets=gets, execs=execs, percent=percent, cpu=cpu, elapsed=elapsed, pdb=pdb))
                a.emit('DBORASQG', d, stack)
            if x == 'SQL ordered by Reads':
                d = dict(timestamp='text', sqlid='text', reads='real', execs='real', percent='real', cpu='real', elapsed='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    reads = tof(y['PhysicalReads']) / a.dur
                    execs = tof(y['Executions']) / a.dur
                    percent = tof(y['%Total'])
                    elapsed = tof(y['ElapsedTime(s)']) / a.dur
                    try: cpu = tof(y['%CPU']) * elapsed
                    except: cpu = tof(y['CPUTime(s)'])
                    sqlid = y['SQLId']
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    a.sqlid[sqlid] = y['SQLModule']
                    stack.append(dict(timestamp=a.date, sqlid=sqlid, reads=reads, execs=execs, percent=percent, cpu=cpu, elapsed=elapsed, pdb=pdb))
                a.emit('DBORASQR', d, stack)
            if x == 'SQL ordered by Executions':
                d = dict(timestamp='text', sqlid='text', execs='real', rows='real', cpuperexec='real', elapsedperexec='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    rows = tof(y['RowsProcessed']) / a.dur
                    execs = tof(y['Executions']) / a.dur
                    try: elapsed = tof(y['ElapsedTime(s)']) / a.dur
                    except: elapsed = tof(y['ElapperExec(s)']) * execs
                    try: cpuperexec = tof(y['%CPU']) * elapsed / execs
                    except: cpuperexec = tof(y['CPUperExec(s)']) * execs
                    elapsedperexec = elapsed / execs
                    sqlid = y['SQLId']
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    a.sqlid[sqlid] = y['SQLModule']
                    stack.append(dict(timestamp=a.date, sqlid=sqlid, execs=execs, rows=rows, cpuperexec=cpuperexec, elapsedperexec=elapsedperexec, pdb=pdb))
                a.emit('DBORASQX', d, stack)
            if x == 'SQL ordered by CPU Time':
                d = dict(timestamp='text', sqlid='text', gets='real', execs='real', cpu='real', elapsed='real', percent='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    cpu = tof(y['CPUTime(s)']) / a.dur
                    elapsed = tof(y['ElapsedTime(s)']) / a.dur
                    execs = tof(y['Executions']) / a.dur
                    try: percent = tof(y['%Total'])
                    except: percent = tof(y['%TotalDBTime'])
                    sqlid = y['SQLId']
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    a.sqlid[sqlid] = y['SQLModule']
                    gets = 0.0
                    stack.append(dict(timestamp=a.date, sqlid=sqlid, gets=gets, execs=execs, cpu=cpu, elapsed=elapsed, percent=percent, pdb=pdb))
                a.emit('DBORASQC', d, stack)
            if x == 'Complete List of SQL Text':
                d = dict(sqlid='text', module='text', request='text')
                stack = []
                for y in a.collected[x]:
                    sqlid = y['SQLId']
                    request = toc(y['SQLText'])
                    module = a.sqlid[sqlid] if sqlid in a.sqlid else ''
                    stack.append(dict(sqlid=sqlid, module=module, request=request))
                a.emit('DBORAREQ', d, stack)
            if x == 'Latch Sleep Breakdown':
                d = dict(timestamp='text', latch='text', gets='real', misses='real', sleeps='real')
                stack = []
                for y in a.collected[x]:
                    latch = y['LatchName']
                    gets = tof(y['GetRequests']) / a.dur
                    misses = tof(y['Misses']) / a.dur
                    sleeps = tof(y['Sleeps']) / a.dur
                    stack.append(dict(timestamp=a.date, latch=latch, gets=gets, misses=misses, sleeps=sleeps))
                a.emit('DBORALAT', d, stack)
            if x == 'Latch Activity':
                d = dict(timestamp='text', latch='text', wait='real')
                stack = []
                for y in a.collected[x]:
                    latch = y['LatchName']
                    wait = tof(y['WaitTime(s)']) / a.dur
                    stack.append(dict(timestamp=a.date, latch=latch, wait=wait))
                a.emit('DBORALAW', d, stack)
            if x == 'Enqueue Activity':
                d = dict(timestamp='text', enqueue='text', requests='real', succgets='real', failedgets='real', waits='real', avgwaitpersec='real')
                stack = []
                for y in a.collected[x]:
                    enqueue = y['EnqueueType(RequestReason)']
                    requests = tof(y['Requests']) / a.dur
                    succgets = tof(y['SuccGets']) / a.dur
                    failedgets = tof(y['FailedGets']) / a.dur
                    waits = tof(y['Waits']) / a.dur
                    avgwaitpersec = tof(y['WtTime(s)']) / a.dur
                    stack.append(dict(timestamp=a.date, enqueue=enqueue, requests=requests, succgets=succgets, failedgets=failedgets, waits=waits, avgwaitpersec=avgwaitpersec))
                a.emit('DBORAENQ', d, stack)
            if x == 'Tablespace IO Stats':
                d = dict(timestamp='text', tablespace='text', reads='real', readtime='real', blocksperread='real', writes='real', busy='real', busytime='real')
                stack = []
                for y in a.collected[x]:
                    tablespace = y['Tablespace']
                    reads = tof(y['Reads']) / a.dur
                    readtime = tof(y['AvRd(ms)'])
                    blocksperread = tof(y['AvBlks/Rd'])
                    writes = tof(y['Writes']) / a.dur
                    busy = tof(y['BufferWaits']) / a.dur
                    busytime = tof(y['AvBufWt(ms)'])
                    stack.append(dict(timestamp=a.date, tablespace=tablespace, reads=reads, readtime=readtime, blocksperread=blocksperread, writes=writes, busy=busy, busytime=busytime))
                a.emit('DBORATBS', d, stack)
            if x == 'File IO Stats':
                d = dict(timestamp='text', tablespace='text', file='text', reads='real', readtime='real', blocksperread='real', writes='real', busy='real', busytime='real')
                stack = []
                for y in a.collected[x]:
                    tablespace = y['Tablespace']
                    file = y['Filename']
                    reads = tof(y['Reads']) / a.dur
                    readtime = tof(y['AvRd(ms)'])
                    blocksperread = tof(y['AvBlks/Rd'])
                    writes = tof(y['Writes']) / a.dur
                    busy = tof(y['BufferWaits']) / a.dur
                    busytime = tof(y['AvBufWt(ms)'])
                    stack.append(dict(timestamp=a.date, tablespace=tablespace, file=file, reads=reads, readtime=readtime, blocksperread=blocksperread, writes=writes, busy=busy, busytime=busytime))
                a.emit('DBORAFIL', d, stack)
            if x == 'SGA breakdown difference' or x == 'SGA breakdown difference by Pool and Name':
                d = dict(timestamp='text', pool='text', name='text', size='real')
                stack = []
                for y in a.collected[x]:
                    pool = toc(y['Pool'])
                    name = y['Name']
                    size = tof(y['EndMB'])
                    stack.append(dict(timestamp=a.date, pool=pool, name=name, size=size))
                a.emit('DBORASGA', d, stack)
            if x == 'PGA Aggr Summary':
                d = dict(timestamp='text', pgahit='real', wamemory='real', extramemory='real')
                stack = []
                for y in a.collected[x]:
                    pgahit = tof(y['PGACacheHit%'])
                    wamemory = tof(y['W/AMBProcessed']) / a.dur
                    extramemory = tof(y['ExtraW/AMBRead/Written']) / a.dur
                    stack.append(dict(timestamp=a.date, pgahit=pgahit, wamemory=wamemory, extramemory=extramemory))
                a.emit('DBORAPGB', d, stack)
            if x == 'PGA Aggr Target Stats':
                d = dict(timestamp='text', aggrtarget='real', autotarget='real', memalloc='real', memused='real')
                stack = []
                for y in a.collected[x]:
                    when = y['@']
                    if when == 'E':
                        aggrtarget = tof(y['PGAAggrTarget(M)'])
                        autotarget = tof(y['AutoPGATarget(M)'])
                        memalloc = tof(y['PGAMemAlloc(M)'])
                        memused = tof(y['W/APGAUsed(M)'])
                        stack.append(dict(timestamp=a.date, aggrtarget=aggrtarget, autotarget=autotarget, memalloc=memalloc, memused=memused))
                a.emit('DBORAPGA', d, stack)
            if x == 'PGA Aggr Target Histogram':
                d = dict(timestamp='text', highoptimal='text', totexecs='real', execs0='real', execs1='real', execs2='real')
                stack = []
                for y in a.collected[x]:
                    highoptimal = y['HighOptimal']
                    totexecs = tof(y['TotalExecs']) / a.dur
                    execs0 = tof(y['OptimalExecs']) / a.dur
                    execs1 = tof(y['1-PassExecs']) / a.dur
                    execs2 = tof(y['M-PassExecs']) / a.dur
                    stack.append(dict(timestamp=a.date, highoptimal=highoptimal, totexecs=totexecs, execs0=execs0, execs1=execs1, execs2=execs2))
                a.emit('DBORAPGC', d, stack)
            if x == 'Operating System Statistics':
                d = dict(timestamp='text', statistic='text', value='real')
                stack = []
                for y in a.collected[x]:
                    statistic = y['Statistic']
                    value = tof(y['Value'])
                    stack.append(dict(timestamp=a.date, statistic=statistic, value=value))
                a.emit('DBORAOSS', d, stack)
            if x == 'Time Model Statistics':
                d = dict(timestamp='text', statistic='text', time='real')
                stack = []
                for y in a.collected[x]:
                    statistic = y['StatisticName']
                    time = tof(y['Time(s)']) / a.dur
                    stack.append(dict(timestamp=a.date, statistic=statistic, time=time))
                a.emit('DBORATMS', d, stack)
            if x == 'Service Statistics':
                d = dict(timestamp='text', service='text', dbtime='real', cpu='real', reads='real', gets='real')
                stack = []
                for y in a.collected[x]:
                    service = y['ServiceName']
                    dbtime = tof(y['DBTime(s)']) / a.dur
                    cpu = tof(y['DBCPU(s)']) / a.dur
                    reads = tof(y['PhysicalReads(K)']) / a.dur
                    gets = tof(y['LogicalReads(K)']) / a.dur
                    stack.append(dict(timestamp=a.date, service=service, dbtime=dbtime, cpu=cpu, reads=reads, gets=gets))
                a.emit('DBORASRV', d, stack)
            if x == 'Service Wait Class Stats':
                d = dict(timestamp='text', service='text', uiowaits='real', uiowaitt='real', conwaits='real', conwaitt='real', admwaits='real', admwaitt='real', netwaits='real', netwaitt='real')
                stack = []
                for y in a.collected[x]:
                    service = y['ServiceName']
                    uiowaits = tof(y['UserI/OTotalWts']) / a.dur
                    uiowaitt = tof(y['UserI/OWtTime']) / a.dur
                    conwaits = tof(y['ConcurcyTotalWts']) / a.dur
                    conwaitt = tof(y['ConcurcyWtTime']) / a.dur
                    admwaits = tof(y['AdminTotalWts']) / a.dur
                    admwaitt = tof(y['AdminWtTime']) / a.dur
                    netwaits = tof(y['NetworkTotalWts']) / a.dur
                    netwaitt = tof(y['NetworkWtTime']) / a.dur
                    stack.append(dict(timestamp=a.date, service=service, uiowaits=uiowaits, uiowaitt=uiowaitt, conwaits=conwaits, conwaitt=conwaitt, admwaits=admwaits, admwaitt=admwaitt, netwaits=netwaits, netwaitt=netwaitt))
                a.emit('DBORASVW', d, stack)
            if x == 'Buffer Pool Statistics':
                d = dict(timestamp='text', bufpool='text', gets='real', reads='real', writes='real', freewaits='real', writecompletewaits='real', busywaits='real')
                stack = []
                for y in a.collected[x]:
                    bufpool = y['P']
                    gets = tof(y['BufferGets']) / a.dur
                    reads = tof(y['PhysicalReads']) / a.dur
                    writes = tof(y['PhysicalWrites']) / a.dur
                    freewaits = tof(y['FreeBuffWait']) / a.dur
                    writecompletewaits = tof(y['WritCompWait']) / a.dur
                    busywaits = tof(y['BufferBusyWaits']) / a.dur
                    stack.append(dict(timestamp=a.date, bufpool=bufpool, gets=gets, reads=reads, writes=writes, freewaits=freewaits, writecompletewaits=writecompletewaits, busywaits=busywaits))
                a.emit('DBORABUF', d, stack)
            if x == 'Buffer Pool Advisory':
                d = dict(timestamp='text', bufpool='text', sizeforest='real', sizefactor='text', buffers='real', estphysreadsfactor='real', estphysreads='real')
                stack = []
                for y in a.collected[x]:
                    bufpool = y['P']
                    sizeforest = tof(y['SizeforEst(M)']) * 1024 * 1024
                    sizefactor = str(tof(y['SizeFactor']))
                    buffers = tof(y['Buffers(thousands)']) * 1000
                    estphysreadsfactor = tof(y['EstPhysReadFactor'])
                    estphysreads = tof(y['EstimatedPhysReads(thousands)']) / a.dur * 1000
                    stack.append(dict(timestamp=a.date, bufpool=bufpool, sizeforest=sizeforest, sizefactor=sizefactor, buffers=buffers, estphysreadsfactor=estphysreadsfactor, estphysreads=estphysreads))
                a.emit('DBORABPA', d, stack)
            if x == 'Segments by Logical Reads':
                d = dict(timestamp='text', owner='text', tablespace='text', object='text', subobject='text', objtype='text', gets='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    owner = y['Owner']
                    tablespace = y['TablespaceName']
                    objname = y['ObjectName']
                    subobject = y['SubobjectName']
                    objtype = y['Obj.Type']
                    gets = tof(y['LogicalReads']) / a.dur
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    stack.append(dict(timestamp=a.date, owner=owner, tablespace=tablespace, object=objname, subobject=subobject, objtype=objtype, gets=gets, pdb=pdb))
                a.emit('DBORASGLR', d, stack)
            if x == 'Segments by Physical Reads':
                d = dict(timestamp='text', owner='text', tablespace='text', object='text', subobject='text', objtype='text', reads='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    owner = y['Owner']
                    tablespace = y['TablespaceName']
                    objname = y['ObjectName']
                    subobject = y['SubobjectName']
                    objtype = y['Obj.Type']
                    reads = tof(y['PhysicalReads']) / a.dur
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    stack.append(dict(timestamp=a.date, owner=owner, tablespace=tablespace, object=objname, subobject=subobject, objtype=objtype, reads=reads, pdb=pdb))
                a.emit('DBORASGPR', d, stack)
            if x == 'Segments by Physical Read Requests':
                d = dict(timestamp='text', owner='text', tablespace='text', object='text', subobject='text', objtype='text', reads='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    owner = y['Owner']
                    tablespace = y['TablespaceName']
                    objname = y['ObjectName']
                    subobject = y['SubobjectName']
                    objtype = y['Obj.Type']
                    reads = tof(y['PhysReadRequests']) / a.dur
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    stack.append(dict(timestamp=a.date, owner=owner, tablespace=tablespace, object=objname, subobject=subobject, objtype=objtype, reads=reads, pdb=pdb))
                a.emit('DBORASGPRR', d, stack)
            if x == 'Segments by UnOptimized Reads':
                d = dict(timestamp='text', owner='text', tablespace='text', object='text', subobject='text', objtype='text', reads='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    owner = y['Owner']
                    tablespace = y['TablespaceName']
                    objname = y['ObjectName']
                    subobject = y['SubobjectName']
                    objtype = y['Obj.Type']
                    reads = tof(y['UnOptimizedReads']) / a.dur
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    stack.append(dict(timestamp=a.date, owner=owner, tablespace=tablespace, object=objname, subobject=subobject, objtype=objtype, reads=reads, pdb=pdb))
                a.emit('DBORASGUR', d, stack)
            if x == 'Segments by Optimized Reads':
                d = dict(timestamp='text', owner='text', tablespace='text', object='text', subobject='text', objtype='text', reads='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    owner = y['Owner']
                    tablespace = y['TablespaceName']
                    objname = y['ObjectName']
                    subobject = y['SubobjectName']
                    objtype = y['Obj.Type']
                    reads = tof(y['OptimizedReads']) / a.dur
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    stack.append(dict(timestamp=a.date, owner=owner, tablespace=tablespace, object=objname, subobject=subobject, objtype=objtype, reads=reads, pdb=pdb))
                a.emit('DBORASGOR', d, stack)
            if x == 'Segments by Direct Physical Reads':
                d = dict(timestamp='text', owner='text', tablespace='text', object='text', subobject='text', objtype='text', reads='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    owner = y['Owner']
                    tablespace = y['TablespaceName']
                    objname = y['ObjectName']
                    subobject = y['SubobjectName']
                    objtype = y['Obj.Type']
                    reads = tof(y['DirectReads']) / a.dur
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    stack.append(dict(timestamp=a.date, owner=owner, tablespace=tablespace, object=objname, subobject=subobject, objtype=objtype, reads=reads, pdb=pdb))
                a.emit('DBORASGDPR', d, stack)
            if x == 'Segments by Physical Writes':
                d = dict(timestamp='text', owner='text', tablespace='text', object='text', subobject='text', objtype='text', writes='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    owner = y['Owner']
                    tablespace = y['TablespaceName']
                    objname = y['ObjectName']
                    subobject = y['SubobjectName']
                    objtype = y['Obj.Type']
                    writes = tof(y['PhysicalWrites']) / a.dur
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    stack.append(dict(timestamp=a.date, owner=owner, tablespace=tablespace, object=objname, subobject=subobject, objtype=objtype, writes=writes, pdb=pdb))
                a.emit('DBORASGPW', d, stack)
            if x == 'Segments by Physical Write Requests':
                d = dict(timestamp='text', owner='text', tablespace='text', object='text', subobject='text', objtype='text', writes='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    owner = y['Owner']
                    tablespace = y['TablespaceName']
                    objname = y['ObjectName']
                    subobject = y['SubobjectName']
                    objtype = y['Obj.Type']
                    writes = tof(y['PhysWriteRequests']) / a.dur
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    stack.append(dict(timestamp=a.date, owner=owner, tablespace=tablespace, object=objname, subobject=subobject, objtype=objtype, writes=writes, pdb=pdb))
                a.emit('DBORASGPWR', d, stack)
            if x == 'Segments by Direct Physical Writes':
                d = dict(timestamp='text', owner='text', tablespace='text', object='text', subobject='text', objtype='text', writes='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    owner = y['Owner']
                    tablespace = y['TablespaceName']
                    objname = y['ObjectName']
                    subobject = y['SubobjectName']
                    objtype = y['Obj.Type']
                    writes = tof(y['DirectWrites']) / a.dur
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    stack.append(dict(timestamp=a.date, owner=owner, tablespace=tablespace, object=objname, subobject=subobject, objtype=objtype, writes=writes, pdb=pdb))
                a.emit('DBORASGDPW', d, stack)
            if x == 'Segments by Table Scans':
                d = dict(timestamp='text', owner='text', tablespace='text', object='text', subobject='text', objtype='text', scans='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    owner = y['Owner']
                    tablespace = y['TablespaceName']
                    objname = y['ObjectName']
                    subobject = y['SubobjectName']
                    objtype = y['Obj.Type']
                    scans = tof(y['TableScans']) / a.dur
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    stack.append(dict(timestamp=a.date, owner=owner, tablespace=tablespace, object=objname, subobject=subobject, objtype=objtype, scans=scans, pdb=pdb))
                a.emit('DBORASGTS', d, stack)
            if x == 'Segments by DB Blocks Changes':
                d = dict(timestamp='text', owner='text', tablespace='text', object='text', subobject='text', objtype='text', changes='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    owner = y['Owner']
                    tablespace = y['TablespaceName']
                    objname = y['ObjectName']
                    subobject = y['SubobjectName']
                    objtype = y['Obj.Type']
                    changes = tof(y['DBBlockChanges']) / a.dur
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    stack.append(dict(timestamp=a.date, owner=owner, tablespace=tablespace, object=objname, subobject=subobject, objtype=objtype, changes=changes, pdb=pdb))
                a.emit('DBORASGDBC', d, stack)
            if x == 'Segments by Row Lock Waits':
                d = dict(timestamp='text', owner='text', tablespace='text', object='text', subobject='text', objtype='text', waits='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    owner = y['Owner']
                    tablespace = y['TablespaceName']
                    objname = y['ObjectName']
                    subobject = y['SubobjectName']
                    objtype = y['Obj.Type']
                    waits = tof(y['RowLockWaits']) / a.dur
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    stack.append(dict(timestamp=a.date, owner=owner, tablespace=tablespace, object=objname, subobject=subobject, objtype=objtype, waits=waits, pdb=pdb))
                a.emit('DBORASGRLW', d, stack)
            if x == 'Segments by ITL Waits':
                d = dict(timestamp='text', owner='text', tablespace='text', object='text', subobject='text', objtype='text', waits='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    owner = y['Owner']
                    tablespace = y['TablespaceName']
                    objname = y['ObjectName']
                    subobject = y['SubobjectName']
                    objtype = y['Obj.Type']
                    waits = tof(y['ITLWaits']) / a.dur
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    stack.append(dict(timestamp=a.date, owner=owner, tablespace=tablespace, object=objname, subobject=subobject, objtype=objtype, waits=waits, pdb=pdb))
                a.emit('DBORASGIW', d, stack)
            if x == 'Segments by Buffer Busy Waits':
                d = dict(timestamp='text', owner='text', tablespace='text', object='text', subobject='text', objtype='text', waits='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    owner = y['Owner']
                    tablespace = y['TablespaceName']
                    objname = y['ObjectName']
                    subobject = y['SubobjectName']
                    objtype = y['Obj.Type']
                    waits = tof(y['BufferBusyWaits']) / a.dur
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    stack.append(dict(timestamp=a.date, owner=owner, tablespace=tablespace, object=objname, subobject=subobject, objtype=objtype, waits=waits, pdb=pdb))
                a.emit('DBORASGBBW', d, stack)
            if x == 'Segments by Global Cache Buffer Busy':
                d = dict(timestamp='text', owner='text', tablespace='text', object='text', subobject='text', objtype='text', waits='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    owner = y['Owner']
                    tablespace = y['TablespaceName']
                    objname = y['ObjectName']
                    subobject = y['SubobjectName']
                    objtype = y['Obj.Type']
                    waits = tof(y['GCBufferBusy']) / a.dur
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    stack.append(dict(timestamp=a.date, owner=owner, tablespace=tablespace, object=objname, subobject=subobject, objtype=objtype, waits=waits, pdb=pdb))
                a.emit('DBORASGGCBB', d, stack)
            if x == 'Segments by CR Blocks Received':
                d = dict(timestamp='text', owner='text', tablespace='text', object='text', subobject='text', objtype='text', blocks='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    owner = y['Owner']
                    tablespace = y['TablespaceName']
                    objname = y['ObjectName']
                    subobject = y['SubobjectName']
                    objtype = y['Obj.Type']
                    blocks = tof(y['CRBlocksReceived']) / a.dur
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    stack.append(dict(timestamp=a.date, owner=owner, tablespace=tablespace, object=objname, subobject=subobject, objtype=objtype, blocks=blocks, pdb=pdb))
                a.emit('DBORASGCRBR', d, stack)
            if x == 'Segments by Current Blocks Received':
                d = dict(timestamp='text', owner='text', tablespace='text', object='text', subobject='text', objtype='text', blocks='real', pdb='text')
                stack = []
                for y in a.collected[x]:
                    owner = y['Owner']
                    tablespace = y['TablespaceName']
                    objname = y['ObjectName']
                    subobject = y['SubobjectName']
                    objtype = y['Obj.Type']
                    blocks = tof(y['CurrentBlocksReceived']) / a.dur
                    pdb = y['PDBName'] if 'PDBName' in y else ''
                    stack.append(dict(timestamp=a.date, owner=owner, tablespace=tablespace, object=objname, subobject=subobject, objtype=objtype, blocks=blocks, pdb=pdb))
                a.emit('DBORASGCBR', d, stack)
            if x == 'Exadata OS CPU Statistics - Top Cells':
                d = dict(timestamp='text', cell='text', cpu='real', usr='real', sys='real')
                stack = []
                for y in a.collected[x]:
                    cell = y['CellName']
                    cpu = tof(y['%CPU'])
                    usr = tof(y['%User'])
                    sys = tof(y['%Sys'])
                    stack.append(dict(timestamp=a.date, cell=cell, cpu=cpu, usr=usr, sys=sys))
                a.emit('EXACPU', d, stack)
            if x == 'Top Databases by IO Requests':
                d = dict(timestamp='text', dbname='text', dbid='text', ptotal='real', totalr='real', flashr='real', diskr='real', totalv='real', flashv='real', diskv='real')
                stack = []
                for y in a.collected[x]:
                    dbname = y['DBName']
                    dbid = y['DBID']
                    ptotal = tof(y['%Total']) if '%Total' in y else tof(y['%Captured'])
                    totalr = tof(y['TotalRequests']) / a.dur
                    flashr = tof(y['Flash']) / a.dur
                    diskr = tof(y['Disk']) / a.dur
                    totalv = tof(y['TotalMB']) / a.dur
                    flashv = tof(y['Flash@']) / a.dur
                    diskv = tof(y['Disk@']) / a.dur
                    stack.append(dict(timestamp=a.date, dbname=dbname, dbid=dbid, ptotal=ptotal, totalr=totalr, flashr=flashr, diskr=diskr, totalv=totalv, flashv=flashv, diskv=diskv))
                a.emit('EXATOPDBIOR', d, stack)
            if x == 'Top Databases by IO Throughput':
                d = dict(timestamp='text', dbname='text', dbid='text', ptotal='real', totalr='real', flashr='real', diskr='real', totalv='real', flashv='real', diskv='real')
                stack = []
                for y in a.collected[x]:
                    dbname = y['DBName']
                    dbid = y['DBID']
                    ptotal = tof(y['%Total']) if '%Total' in y else tof(y['%Captured'])
                    totalr = tof(y['TotalRequests']) / a.dur
                    flashr = tof(y['Flash@']) / a.dur
                    diskr = tof(y['Disk@']) / a.dur
                    totalv = tof(y['TotalMB']) / a.dur
                    flashv = tof(y['Flash']) / a.dur
                    diskv = tof(y['Disk']) / a.dur
                    stack.append(dict(timestamp=a.date, dbname=dbname, dbid=dbid, ptotal=ptotal, totalr=totalr, flashr=flashr, diskr=diskr, totalv=totalv, flashv=flashv, diskv=diskv))
                a.emit('EXATOPDBIOV', d, stack)
            if x == 'Exadata Cell Server IOPS - Top Disks':
                d = dict(timestamp='text', type='text', cell='text', name='text', ptotal='real', average='real', smallr='real', smallw='real', larger='real', largew='real')
                stack = []
                for y in a.collected[x]:
                    type = y['DiskType']
                    cell = y['CellName']
                    name = y['DiskName']
                    ptotal = tof(y['%Total'])
                    average = tof(y['Average'])
                    smallr = tof(y['SmallReads'])
                    smallw = tof(y['SmallWrites'])
                    larger = tof(y['LargeReads'])
                    largew = tof(y['LargeWrites'])
                    stack.append(dict(timestamp=a.date, type=type, cell=cell, name=name, ptotal=ptotal, average=average, smallr=smallr, smallw=smallw, larger=larger, largew=largew))
                a.emit('EXATOPDSKIOR', d, stack)
            if x == 'Exadata Cell Server IO MB/s - Top Disks':
                d = dict(timestamp='text', type='text', cell='text', name='text', ptotal='real', average='real', smallr='real', smallw='real', larger='real', largew='real')
                stack = []
                for y in a.collected[x]:
                    type = y['DiskType']
                    cell = y['CellName']
                    name = y['DiskName']
                    ptotal = tof(y['%Total'])
                    average = tof(y['Average'])
                    smallr = tof(y['SmallReads'])
                    smallw = tof(y['SmallWrites'])
                    larger = tof(y['LargeReads'])
                    largew = tof(y['LargeWrites'])
                    stack.append(dict(timestamp=a.date, type=type, cell=cell, name=name, ptotal=ptotal, average=average, smallr=smallr, smallw=smallw, larger=larger, largew=largew))
                a.emit('EXATOPDSKIOV', d, stack)
            if x == 'Exadata OS IO Statistics - Top Cells':
                d = dict(timestamp='text', type='text', cell='text', prtotal='real', raverage='real', pvtotal='real', vaverage='real', putil='real')
                stack = []
                for y in a.collected[x]:
                    type = y['DiskType']
                    cell = y['CellName']
                    prtotal = tof(y['%Total'])
                    raverage = tof(y['Avg'])
                    pvtotal = tof(y['%Total@'])
                    vaverage = tof(y['Avg@'])
                    putil = tof(y['Avg@@'])
                    stack.append(dict(timestamp=a.date, type=type, cell=cell, prtotal=prtotal, raverage=raverage, pvtotal=pvtotal, vaverage=vaverage, putil=putil))
                a.emit('EXATOPCLLOSIO', d, stack)
            if x == 'Exadata OS IO Statistics - Top Disks':
                d = dict(timestamp='text', type='text', cell='text', disk='text', prtotal='real', raverage='real', pvtotal='real', vaverage='real', putil='real')
                stack = []
                for y in a.collected[x]:
                    type = y['DiskType']
                    disk = y['DiskName']
                    cell = y['CellName']
                    prtotal = tof(y['%Total'])
                    raverage = tof(y['Avg'])
                    pvtotal = tof(y['%Total@'])
                    vaverage = tof(y['Avg@'])
                    putil = tof(y['Avg@@'])
                    stack.append(dict(timestamp=a.date, type=type, cell=cell, disk=disk, prtotal=prtotal, raverage=raverage, pvtotal=pvtotal, vaverage=vaverage, putil=putil))
                a.emit('EXATOPDSKOSIO', d, stack)
            if x == 'Exadata OS IO Latency - Top Cells':
                d = dict(timestamp='text', type='text', cell='text', stime='real', wtime='real')
                stack = []
                for y in a.collected[x]:
                    type = y['DiskType']
                    cell = y['CellName']
                    stime = tof(y['ServiceTime'].replace('us', '')) /1000 if 'us' in y['ServiceTime'] else tof(y['ServiceTime'].replace('ms', ''))
                    wtime = tof(y['WaitTime'].replace('us', '')) /1000 if 'us' in y['WaitTime'] else tof(y['WaitTime'].replace('ms', ''))
                    stack.append(dict(timestamp=a.date, type=type, cell=cell, stime=stime, wtime=wtime))
                a.emit('EXATOPCLLOSIOL', d, stack)
            if x == 'Exadata OS IO Latency - Top Disks':
                d = dict(timestamp='text', type='text', cell='text', disk='text', stime='real', wtime='real')
                stack = []
                for y in a.collected[x]:
                    type = y['DiskType']
                    disk = y['DiskName']
                    cell = y['CellName']
                    stime = tof(y['ServiceTime'].replace('us', '')) /1000 if 'us' in y['ServiceTime'] else tof(y['ServiceTime'].replace('ms', ''))
                    wtime = tof(y['WaitTime'].replace('us', '')) /1000 if 'us' in y['WaitTime'] else tof(y['WaitTime'].replace('ms', ''))
                    stack.append(dict(timestamp=a.date, type=type, cell=cell, disk=disk, stime=stime, wtime=wtime))
                a.emit('EXATOPDSKOSIOL', d, stack)

    def aaction(self, a, l, g, m):
        if l.tag in ['h3', 'h4']: self.ah3(a, l, g, m)
        if l.tag in ['th', 'td']: self.athd(a, l, g, m)
        if l.tag in ['table']: self.atable(a, l, g, m)
        if l.tag in ['tr']: self.atr(a, l, g, m)

    def ah3(self, a, l, g, m):
        context = ''
        a.setContext(context)
        if len(a.row): a.tab.append(a.row)
        a.row = {}

    def atable(self, a, l, g, m):
        context = ''
        if a.reinit: a.setContext(context)
        if len(a.scope) < 3:
            if a.scope.issubset({'DBORAINFO', 'DBORAMISC'}) and 'zz9' in a.collected and 'zz8' in a.collected: a.setContext('BREAK')
            if a.scope.issubset({'DBORAWEV'}) and 'Foreground Wait Events' in a.collected and len(a.collected['Foreground Wait Events']): a.setContext('BREAK')
            if a.scope.issubset({'DBORAWEB'}) and 'Background Wait Events' in a.collected and len(a.collected['Background Wait Events']): a.setContext('BREAK')
            if a.scope.issubset({'DBORAWEC'}) and 'Foreground Wait Class' in a.collected and len(a.collected['Foreground Wait Class']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASTA'}) and 'Instance Activity Stats - Thread Activity' in a.collected and len(a.collected['Instance Activity Stats - Thread Activity']): a.setContext('BREAK')
            if a.scope.issubset({'DBORAMDC'}) and 'Memory Dynamic Components' in a.collected and len(a.collected['Memory Dynamic Components']): a.setContext('BREAK')
            if a.scope.issubset({'DBORAMTT'}) and 'Instance Recovery Stats' in a.collected and len(a.collected['Instance Recovery Stats']): a.setContext('BREAK')
            if a.scope.issubset({'DBORALIB'}) and 'Library Cache Activity' in a.collected and len(a.collected['Library Cache Activity']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASQE'}) and 'SQL ordered by Elapsed Time' in a.collected and len(a.collected['SQL ordered by Elapsed Time']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASQP'}) and 'SQL ordered by Parse Calls' in a.collected and len(a.collected['SQL ordered by Parse Calls']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASQM'}) and 'SQL ordered by Sharable Memory' in a.collected and len(a.collected['SQL ordered by Sharable Memory']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASQV'}) and 'SQL ordered by Version Count' in a.collected and len(a.collected['SQL ordered by Version Count']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASQW'}) and 'SQL ordered by Cluster Wait Time' in a.collected and len(a.collected['SQL ordered by Cluster Wait Time']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASQG'}) and 'SQL ordered by Gets' in a.collected and len(a.collected['SQL ordered by Gets']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASQR'}) and 'SQL ordered by Reads' in a.collected and len(a.collected['SQL ordered by Reads']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASQX'}) and 'SQL ordered by Executions' in a.collected and len(a.collected['SQL ordered by Executions']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASQC'}) and 'SQL ordered by CPU Time' in a.collected and len(a.collected['SQL ordered by CPU Time']): a.setContext('BREAK')
            if a.scope.issubset({'DBORAREQ'}) and 'Complete List of SQL Text' in a.collected and len(a.collected['Complete List of SQL Text']): a.setContext('BREAK')
            if a.scope.issubset({'DBORALAT'}) and 'Latch Sleep Breakdown' in a.collected and len(a.collected['Latch Sleep Breakdown']): a.setContext('BREAK')
            if a.scope.issubset({'DBORALAW'}) and 'Latch Activity' in a.collected and len(a.collected['Latch Activity']): a.setContext('BREAK')
            if a.scope.issubset({'DBORAENQ'}) and 'Enqueue Activity' in a.collected and len(a.collected['Enqueue Activity']): a.setContext('BREAK')
            if a.scope.issubset({'DBORATBS'}) and 'Tablespace IO Stats' in a.collected and len(a.collected['Tablespace IO Stats']): a.setContext('BREAK')
            if a.scope.issubset({'DBORAFIL'}) and 'File IO Stats' in a.collected and len(a.collected['File IO Stats']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASGA'}) and 'SGA breakdown difference' in a.collected and len(a.collected['SGA breakdown difference']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASGA'}) and 'SGA breakdown difference by Pool and Name' in a.collected and len(a.collected['SGA breakdown difference by Pool and Name']): a.setContext('BREAK')
            if a.scope.issubset({'DBORAPGB'}) and 'PGA Aggr Summary' in a.collected and len(a.collected['PGA Aggr Summary']): a.setContext('BREAK')
            if a.scope.issubset({'DBORAPGA'}) and 'PGA Aggr Target Stats' in a.collected and len(a.collected['PGA Aggr Target Stats']): a.setContext('BREAK')
            if a.scope.issubset({'DBORAPGC'}) and 'PGA Aggr Target Histogram' in a.collected and len(a.collected['PGA Aggr Target Histogram']): a.setContext('BREAK')
            if a.scope.issubset({'DBORAOSS'}) and 'Operating System Statistics' in a.collected and len(a.collected['Operating System Statistics']): a.setContext('BREAK')
            if a.scope.issubset({'DBORATMS'}) and 'Time Model Statistics' in a.collected and len(a.collected['Time Model Statistics']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASRV'}) and 'Service Statistics' in a.collected and len(a.collected['Service Statistics']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASVW'}) and 'Service Wait Class Stats' in a.collected and len(a.collected['Service Wait Class Stats']): a.setContext('BREAK')
            if a.scope.issubset({'DBORABUF'}) and 'Buffer Pool Statistics' in a.collected and len(a.collected['Buffer Pool Statistics']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASGLR'}) and 'Segments by Logical Reads' in a.collected and len(a.collected['Segments by Logical Reads']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASGPR'}) and 'Segments by Physical Reads' in a.collected and len(a.collected['Segments by Physical Reads']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASGRW'}) and 'Segments by Row Lock Waits' in a.collected and len(a.collected['Segments by Row Lock Waits']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASGIW'}) and 'Segments by ITL Waits' in a.collected and len(a.collected['Segments by ITL Waits']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASGFSC'}) and 'Segments by Table Scans' in a.collected and len(a.collected['Segments by Table Scans']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASGBB'}) and 'Segments by Buffer Busy Waits' in a.collected and len(a.collected['Segments by Buffer Busy Waits']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASGGB'}) and 'Segments by Global Cache Buffer Busy' in a.collected and len(a.collected['Segments by Global Cache Buffer Busy']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASGCR'}) and 'Segments by CR Blocks Received' in a.collected and len(a.collected['Segments by CR Blocks Received']): a.setContext('BREAK')
            if a.scope.issubset({'DBORASGCB'}) and 'Segments by Current Blocks Received' in a.collected and len(a.collected['Segments by Current Blocks Received']): a.setContext('BREAK')
            if a.scope.issubset({'EXACPU'}) and 'Exadata OS CPU Statistics - Top Cells' in a.collected and len(a.collected['Exadata OS CPU Statistics - Top Cells']): a.setContext('BREAK')
            if a.scope.issubset({'EXATOPDBIOR'}) and 'Top Databases by IO Requests' in a.collected and len(a.collected['Top Databases by IO Requests']): a.setContext('BREAK')
            if a.scope.issubset({'EXATOPDBIOV'}) and 'Top Databases by IO Throughput' in a.collected and len(a.collected['Top Databases by IO Throughput']): a.setContext('BREAK')
            if a.scope.issubset({'EXATOPDSKIOR'}) and 'Exadata Cell Server IOPS - Top Disks' in a.collected and len(a.collected['Exadata Cell Server IOPS - Top Disks']): a.setContext('BREAK')
            if a.scope.issubset({'EXATOPDSKIOV'}) and 'Exadata Cell Server IO MB/s - Top Disks' in a.collected and len(a.collected['Exadata Cell Server IO MB/s - Top Disks']): a.setContext('BREAK')
            if a.scope.issubset({'EXATOPCLLOSIO'}) and 'Exadata OS IO Statistics - Top Cells' in a.collected and len(a.collected['Exadata OS IO Statistics - Top Cells']): a.setContext('BREAK')
            if a.scope.issubset({'EXATOPDSKOSIO'}) and 'Exadata OS IO Statistics - Top Disks' in a.collected and len(a.collected['Exadata OS IO Statistics - Top Disks']): a.setContext('BREAK')
            if a.scope.issubset({'EXATOPCLLOSIOL'}) and 'Exadata OS IO Latency - Top Cells' in a.collected and len(a.collected['Exadata OS IO Latency - Top Cells']): a.setContext('BREAK')
            if a.scope.issubset({'EXATOPDSKOSIOL'}) and 'Exadata OS IO Latency - Top Disks' in a.collected and len(a.collected['Exadata OS IO Latency - Top Disks']): a.setContext('BREAK')
        if len(a.row): a.tab.append(a.row)
        a.row = {}
        a.collector = {}

    def athget(self, a, l, g, m):
        if 0 not in a.collector: a.collector[0] = ''
        x = a.lxmltext(l).replace(' ', '')
        a.collector[a.cpt] = x if x not in a.collector.values() else x + '@' if x + '@' not in a.collector.values() else x + '@@'
        #a.collector[a.cpt]=a.lxmltext(l)

    def atdget(self, a, l, g, m):
        if a.cpt in a.collector: a.row[a.collector[a.cpt]]=a.lxmltext(l) if a.lxmltext(l) != '' else a.memory[a.collector[a.cpt]] if a.collector[a.cpt] in a.memory and 'exatop' in a.context else ''

    def atr(self, a, l, g, m):
        a.reinit = True
        a.cpt = -1
        if hasattr(a,'collector') and len(a.collector): a.setContext('td'+a.context[2:])
        if len(a.row): a.tab.append(a.row)
        a.memory = a.row
        a.row = {}

    def athd(self, a, l, g, m):
        colspan = int(l.attrib['colspan']) if 'colspan' in l.attrib else 1
        a.cpt+=colspan

    def genstate(self, c):
        def f(a, l ,g, m):
            a.reinit = False
            a.setContext(c)
            a.tab = []
            k = a.lxmltext(l)
            if re.match('Snap.*Cursors/Session', k): k = 'zz9'
            if re.match('DB Name.*ReleaseRAC', k): k = 'zz8'
            if re.match('InstanceInst.*Time', k): k = 'zz7'
            if re.match('Container DB Id', k): k = 'zz6'
            a.collected[k] = a.tab
        return f
