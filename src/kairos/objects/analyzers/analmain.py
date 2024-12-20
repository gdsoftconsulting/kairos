class UserObject(dict):
    def __init__(self):
        object = {
            "type": "analyzer",
            "id": "ANALMAIN",
            "begin": self.begin,
            "end": self.end,
            "outcontextrules": [],
            "contextrules": [
                {"context": "gentype", "action": self.gentype, "regexp": r'^\w+\s(\w+)\s+'}
            ],
            "rules": [
                {"action": self.awrhtml, "regexp": r'.[Hh][Ee][Aa][Dd].<[Tt][Ii][Tt][Ll][Ee]>AWR Report for DB:'},
                {"action": self.awrpdb, "regexp": r'summary="This table displays pdb instance information"'},
                {"action": self.awrrachtml, "regexp": r'.head.<title>AWR RAC Report for DB:'},
                {"action": self.astatspack, "regexp": r'(^STATSPACK Statistics Report for|^STATSPACK report for)'},
                {"action": self.awr, "regexp": r'^WORKLOAD REPOSITORY report for'},
                {"action": self.ebs, "regexp": r'^REPORT TYPE: EBS12CM'},
                {"action": self.bo, "regexp": r'^REPORT TYPE: BO'},
                {"action": self.gen, "regexp": r'^REPORT TYPE: (\w+) '},
                {"action": self.json, "regexp": r'^\s+"collection":\s*"(\w+)'},
                {"action": self.nmon, "regexp": r'^AAA,progname,'},
                {"action": self.nmon, "regexp": r'^CPU_ALL,'},
                {"action": self.vmstat, "regexp": r'Collection Module:.+VmstatExaWatcher'},
                {"action": self.meminfo, "regexp": r'Collection Module:.+MeminfoExaWatcher'},
                {"action": self.tthtml, "regexp": r'.<[Tt][Ii][Tt][Ll][Ee]>TTSTATS REPORT'},
                {"action": self.sar, "regexp": r'^(AIX|SunOS|HP-UX|Linux)[ \t]+(.+?)[ \t]+.*[ \t]+[0-9][0-9]/[0-9][0-9]/2?0?[0-9][0-9].*$'},
                {"action": self.snapper, "regexp": r'^ +ActSes +%Thread'},
                {"action": self.snapper, "regexp": r'No active sessions captured during the sampling period'},
                {"action": self.t10046, "regexp": r'^Trace file '},
                {"action": self.stop, "regexp": r'^'}
            ]
        }
        super(UserObject, self).__init__(**object)

    def begin(self, a):
        a.cpt = 0
        a.awrhtml = False
        a.awrpdb = False
        a.member = None

    def end(self, a):
        if a.awrhtml:
            if a.awrpdb: a.emit(None, None, {
                            "member": a.member,
                            "analyzer": 'ANALAWRHTML',
                            "collections": ['DBORAPDB', 'DBORAAWR', 'DBORAINFO', 'DBORAMISC', 'DBORAMDC', 'DBORABPA', 'DBORAWEC', 'DBORAWEV', 'DBORAWEB', 'DBORASTA', 'DBORAMTT', 'DBORALIB', 'DBORASQE', 'DBORASQP', 'DBORASQM', 'DBORASQV', 'DBORASQW', 'DBORASQG', 'DBORASQR', 'DBORASQX', 'DBORASQC', 'DBORAREQ', 'DBORALAT', 'DBORALAW', 'DBORAENQ', 'DBORATBS', 'DBORAFIL', 'DBORASGA', 'DBORAPGA', 'DBORAPGB', 'DBORAPGC', 'DBORAOSS', 'DBORATMS', 'DBORASRV', 'DBORASVW', 'DBORABUF', 'DBORASGLR', 'DBORASGPR', 'DBORASGPRR', 'DBORASGUR', 'DBORASGOR', 'DBORASGDPR', 'DBORASGPW', 'DBORASGPWR', 'DBORASGDPW', 'DBORASGTS', 'DBORASGDBC', 'DBORASGRLW', 'DBORASGIW', 'DBORASGBBW', 'DBORASGGCBB', 'DBORASGCRBR', 'DBORASGCBR', 'EXACPU', 'EXATOPDBIOR', 'EXATOPDBIOV', 'EXATOPDSKIOR', 'EXATOPDSKIOV', 'EXATOPCLLOSIO', 'EXATOPCLLOSIOL', 'EXATOPDSKOSIO', 'EXATOPDSKOSIOL']
                        })
            else: a.emit(None, None, {
                    "member": a.member,
                    "analyzer": 'ANALAWRHTML',
                    "collections": ['DBORAAWR', 'DBORAINFO', 'DBORAMISC', 'DBORAMDC', 'DBORABPA', 'DBORAWEC', 'DBORAWEV', 'DBORAWEB', 'DBORASTA', 'DBORAMTT', 'DBORALIB', 'DBORASQE', 'DBORASQP', 'DBORASQM', 'DBORASQV', 'DBORASQW', 'DBORASQG', 'DBORASQR', 'DBORASQX', 'DBORASQC', 'DBORAREQ', 'DBORALAT', 'DBORALAW', 'DBORAENQ', 'DBORATBS', 'DBORAFIL', 'DBORASGA', 'DBORAPGA', 'DBORAPGB', 'DBORAPGC', 'DBORAOSS', 'DBORATMS', 'DBORASRV', 'DBORASVW', 'DBORABUF', 'DBORASGLR', 'DBORASGPR', 'DBORASGPRR', 'DBORASGUR', 'DBORASGOR', 'DBORASGDPR', 'DBORASGPW', 'DBORASGPWR', 'DBORASGDPW', 'DBORASGTS', 'DBORASGDBC', 'DBORASGRLW', 'DBORASGIW', 'DBORASGBBW', 'DBORASGGCBB', 'DBORASGCRBR', 'DBORASGCBR', 'EXACPU', 'EXATOPDBIOR', 'EXATOPDBIOV', 'EXATOPDSKIOR', 'EXATOPDSKIOV', 'EXATOPCLLOSIO', 'EXATOPCLLOSIOL', 'EXATOPDSKOSIO', 'EXATOPDSKOSIOL']
                })

    def awr(self, a, l ,g, m):
        if not a.awrhtml:
            a.setContext('BREAK')
            a.emit(None, None, {
                "member": m,
                "analyzer": "ANALAWR",
                "collections": ['DBORAAWR', 'DBORAINFO', 'DBORAMISC', 'DBORAMDC', 'DBORADRV', 'DBORAWEC', 'DBORAWEV', 'DBORAWEB', 'DBORASTA', 'DBORAMTT', 'DBORALIB', 'DBORASQE', 'DBORASQP', 'DBORASQM', 'DBORASQV', 'DBORASQW', 'DBORASQG', 'DBORASQR', 'DBORASQX', 'DBORASQC', 'DBORAREQ', 'DBORALAT', 'DBORALAW', 'DBORAENQ', 'DBORATBS', 'DBORAFIL', 'DBORASGA', 'DBORAPGA', 'DBORAPGB', 'DBORAPGC', 'DBORAOSS', 'DBORATMS', 'DBORASRV', 'DBORASVW', 'DBORABUF', 'DBORASGLR', 'DBORASGPR', 'DBORASGPRR', 'DBORASGUR', 'DBORASGOR', 'DBORASGDPR', 'DBORASGPW', 'DBORASGPWR', 'DBORASGDPW', 'DBORASGTS', 'DBORASGDBC', 'DBORASGRLW', 'DBORASGIW', 'DBORASGBBW', 'DBORASGGCBB', 'DBORASGCRBR', 'DBORASGCBR']
            })

    def astatspack(self, a, l ,g, m):
        a.setContext('BREAK')
        a.emit(None, None, {
            "member": m,
            "analyzer": "ANALSP",
            "collections": ['DBORASTATSPACK', 'DBORAINFO', 'DBORAMISC', 'DBORAMDC', 'DBORADRV', 'DBORAWEC', 'DBORAWEV', 'DBORAWEB', 'DBORASTA', 'DBORAMTT', 'DBORALIB', 'DBORASQE', 'DBORASQP', 'DBORASQM', 'DBORASQV', 'DBORASQW', 'DBORASQG', 'DBORASQR', 'DBORASQX', 'DBORASQC', 'DBORAREQ', 'DBORALAT', 'DBORALAW', 'DBORAENQ', 'DBORATBS', 'DBORAFIL', 'DBORASGA', 'DBORAPGA', 'DBORAPGB', 'DBORAPGC', 'DBORAOSS', 'DBORATMS', 'DBORASRV', 'DBORASVW', 'DBORABUF', 'DBORASGLR', 'DBORASGPR', 'DBORASGPRR', 'DBORASGUR', 'DBORASGOR', 'DBORASGDPR', 'DBORASGPW', 'DBORASGPWR', 'DBORASGDPW', 'DBORASGTS', 'DBORASGDBC', 'DBORASGRLW', 'DBORASGIW', 'DBORASGBBW', 'DBORASGGCBB', 'DBORASGCRBR', 'DBORASGCBR']
        })

    def tthtml(self, a, l ,g, m):
        a.setContext('BREAK')
        a.emit(None, None, {
            "member": m,
            "analyzer": "ANALTTHTML",
            "collections": ['TTMISC', 'TTSTATS', 'TTPARAM', 'TTSQLTOPP', 'TTSQLTOPX', 'TTSQLTEXT', 'TTABSMETRICS', 'TTMETRICS']
        })

    def awrhtml(self, a, l, g, m):
        a.awrhtml = True
        a.member = m

    def awrpdb(self, a, l, g, m):
        a.awrpdb = True
        a.setContext('BREAK')
        
    def vmstat(self, a, l, g, m):
        a.setContext('BREAK')
        a.emit(None, None, {
            "member": m,
            "analyzer": 'ANALVMSTAT',
            "collections": ['VMSTAT']
        })
        
    def meminfo(self, a, l, g, m):
        a.setContext('BREAK')
        a.emit(None, None, {
            "member": m,
            "analyzer": 'ANALMEMINFO',
            "collections": ['MEMINFO']
        })
        
    def snapper(self, a, l, g, m):
        a.setContext('BREAK')
        a.emit(None, None, {
            "member": m,
            "analyzer": 'ANALSNAPPER',
            "collections": ['SNAPPER']
        })
        
    def t10046(self, a, l, g, m):
        a.setContext('BREAK')
        a.emit(None, None, {
            "member": m,
            "analyzer": 'ANALT10046',
            "collections": ['TPARSING', 'TPARSE', 'TEXEC', 'TFETCH', 'TCLOSE', 'TSTAT', 'TBINDS', 'TWAIT','TERROR','TXCTEND']
        })

    def awrrachtml(self, a, l, g, m):
        a.setContext('BREAK')
        a.emit(None, None, {
            "member": m,
            "analyzer": 'ANALAWRRACHTML',
            "collections": ['DBORARACMISC', 'DBORARACCSIZE', 'DBORARACOSS', 'DBORARACTM', 'DBORARACFWC', 'DBORARACTTE', 'DBORARACTTFE', 'DBORARACTTBE', 'DBORARACGALPSS', 'DBORARACGALPGM', 'DBORARACGCEP', 'DBORARACGCTS', 'DBORARACSTA', 'DBORARACSTAA', 'DBORARACSEG', 'DBORARACPING', 'DBORARACREQ', 'DBORARACSQE', 'DBORARACSQC', 'DBORARACSQI', 'DBORARACSQG', 'DBORARACSQR', 'DBORARACSQU', 'DBORARACSQX', 'DBORARACSQW']
        })

    def gen(self, a, l, g, m):
        a.setContext('gentype')

    def gentype(self, a, l, g, m):
        a.setContext('BREAK')
        a.emit(None, None, {
            "member": m,
            "analyzer": 'ANALGEN',
            "collections": [g(1)]
        })

    def json(self, a, l, g, m):
        a.setContext('BREAK')
        a.emit(None, None, {
            "member": m,
            "analyzer": 'ANALJSON',
            "collections": [g(1)]
        })

    def ebs(self, a, l, g, m):
        a.setContext('BREAK')
        a.emit(None, None, {
            "member": m,
            "analyzer": 'ANALEBS',
            "collections": ['EBS12CM']
        })

    def bo(self, a, l, g, m):
        a.setContext('BREAK')
        a.emit(None, None, {
            "member": m,
            "analyzer": 'ANALBO',
            "collections": ['BO']
        })

    def nmon(self, a, l ,g, m):
        a.setContext('BREAK')
        a.emit(None, None, {
            "member": m,
            "analyzer": "ANALNMON",
            "collections": ['NMONCPU', 'NMONDISKBSIZE', 'NMONDISKBUSY', 'NMONDISKREAD', 'NMONDISKSERV', 'NMONDISKWAIT', 'NMONDISKWRITE', 'NMONDISKXFER', 'NMONDISKRIO', 'NMONDISKWIO', 'NMONDGBUSY', 'NMONDGREAD', 'NMONDGWRITE', 'NMONDGXFER', 'NMONDGSIZE', 'NMONFILE', 'NMONIOADAPT', 'NMONJFSFILE', 'NMONJFSINODE', 'NMONLARGEPAGE', 'NMONLPAR', 'NMONMEM', 'NMONMEMNEW', 'NMONMEMUSE', 'NMONNET', 'NMONNETERROR', 'NMONNETPACKET', 'NMONNETSIZE', 'NMONNFSCLIV2', 'NMONNFSCLIV3', 'NMONNFSSVRV2', 'NMONNFSSVRV3', 'NMONPAGE', 'NMONPOOLS', 'NMONPROC', 'NMONPROCAIO', 'NMONVM', 'NMONTOP', 'NMONAAA']
        })

    def sar(self, a, l ,g, m):
        a.setContext('BREAK')
        a.emit(None, None, {
            "member": m,
            "analyzer": "ANALSAR",
            "collections": ['SARB', 'SARD', 'SARM', 'SARN', 'SARP', 'SARQ', 'SARU', 'SARV', 'SARW']
        })

    def stop(self, a, l, g, m):
        a.cpt += 1
        if (a.cpt > 99): a.setContext('BREAK')
