class UserObject(dict):
    def __init__(self):
        object = {
            "type": "analyzer",
            "id": "ANALNMON",
            "begin": self.begin,
            "end": self.end,
            "rules": [],
            "contextrules": [
            ],
            "outcontextrules": [
                {"action": self.gettimestamp, "regexp": r'^ZZZZ,(T\d+),(\d+):(\d+):(\d+),(\d+)-(\w+)-(\d+)'},
                {"action": self.getcpuval, "regexp": r'^(CPU\d+),(T\d+),(.+?),(.+?),(.+?),(.+?)$', "scope": "NMONCPU"},
                {"action": self.getcpuall, "regexp": r'^CPU_ALL,(T\d+),(.+?),(.+?),(.+?),(.+?),(.*?),(.+?)$', "scope": "NMONCPU"},
                {"action": self.genc2("NMONDISKBSIZE"), "regexp": r'^DISKBSIZE([1-9]*),Disk .*?,(.+)$', "scope": "NMONDISKBSIZE"},
                {"action": self.genv2("NMONDISKBSIZE"), "regexp": r'^DISKBSIZE([1-9]*),(T\d+),(.+)$', "scope": "NMONDISKBSIZE"},
                {"action": self.genc2("NMONDISKBUSY"), "regexp": r'^DISKBUSY([1-9]*),Disk .*?,(.+)$', "scope": "NMONDISKBUSY"},
                {"action": self.genv2("NMONDISKBUSY"), "regexp": r'^DISKBUSY([1-9]*),(T\d+),(.+)$', "scope": "NMONDISKBUSY"},
                {"action": self.genc2("NMONDISKREAD"), "regexp": r'^DISKREAD([1-9]*),Disk .*?,(.+)$', "scope": "NMONDISKREAD"},
                {"action": self.genv2("NMONDISKREAD"), "regexp": r'^DISKREAD([1-9]*),(T\d+),(.+)$', "scope": "NMONDISKREAD"},
                {"action": self.genc2("NMONDISKSERV"), "regexp": r'^DISKSERV([1-9]*),Disk .*?,(.+)$', "scope": "NMONDISKSERV"},
                {"action": self.genv2("NMONDISKSERV"), "regexp": r'^DISKSERV([1-9]*),(T\d+),(.+)$', "scope": "NMONDISKSERV"},
                {"action": self.genc2("NMONDISKWAIT"), "regexp": r'^DISKWAIT([1-9]*),Disk .*?,(.+)$', "scope": "NMONDISKWAIT"},
                {"action": self.genc2("NMONDISKWAIT"), "regexp": r'^DISKWAIT([1-9]*),Average .*?,(.+)$', "scope": "NMONDISKWAIT"},
                {"action": self.genv2("NMONDISKWAIT"), "regexp": r'^DISKWAIT([1-9]*),(T\d+),(.+)$', "scope": "NMONDISKWAIT"},
                {"action": self.genc2("NMONDISKWRITE"), "regexp": r'^DISKWRITE([1-9]*),Disk .*?,(.+)$', "scope": "NMONDISKWRITE"},
                {"action": self.genv2("NMONDISKWRITE"), "regexp": r'^DISKWRITE([1-9]*),(T\d+),(.+)$', "scope": "NMONDISKWRITE"},
                {"action": self.genc2("NMONDISKXFER"), "regexp": r'^DISKXFER([1-9]*),Disk .*?,(.+)$', "scope": "NMONDISKXFER"},
                {"action": self.genv2("NMONDISKXFER"), "regexp": r'^DISKXFER([1-9]*),(T\d+),(.+)$', "scope": "NMONDISKXFER"},
                {"action": self.genc2("NMONDISKRIO"), "regexp": r'^DISKRIO([1-9]*),Disk .*?,(.+)$', "scope": "NMONDISKRIO"},
                {"action": self.genv2("NMONDISKRIO"), "regexp": r'^DISKRIO([1-9]*),(T\d+),(.+)$', "scope": "NMONDISKRIO"},
                {"action": self.genc2("NMONDISKWIO"), "regexp": r'^DISKWIO([1-9]*),Disk .*?,(.+)$', "scope": "NMONDISKWIO"},
                {"action": self.genv2("NMONDISKWIO"), "regexp": r'^DISKWIO([1-9]*),(T\d+),(.+)$', "scope": "NMONDISKWIO"},
                {"action": self.genc1("NMONDGBUSY"), "regexp": r'^DGBUSY,Disk .*?,(.+)$', "scope": "NMONDGBUSY"},
                {"action": self.genv1("NMONDGBUSY"), "regexp": r'^DGBUSY,(T\d+),(.+)$', "scope": "NMONDGBUSY"},
                {"action": self.genc1("NMONDGREAD"), "regexp": r'^DGREAD,Disk .*?,(.+)$', "scope": "NMONDGREAD"},
                {"action": self.genv1("NMONDGREAD"), "regexp": r'^DGREAD,(T\d+),(.+)$', "scope": "NMONDGREAD"},
                {"action": self.genc1("NMONDGWRITE"), "regexp": r'^DGWRITE,Disk .*?,(.+)$', "scope": "NMONDGWRITE"},
                {"action": self.genv1("NMONDGWRITE"), "regexp": r'^DGWRITE,(T\d+),(.+)$', "scope": "NMONDGWRITE"},
                {"action": self.genc1("NMONDGXFER"), "regexp": r'^DGXFER,Disk .*?,(.+)$', "scope": "NMONDGXFER"},
                {"action": self.genv1("NMONDGXFER"), "regexp": r'^DGXFER,(T\d+),(.+)$', "scope": "NMONDGXFER"},
                {"action": self.genc1("NMONDGSIZE"), "regexp": r'^DGSIZE,Disk .*?,(.+)$', "scope": "NMONDGSIZE"},
                {"action": self.genv1("NMONDGSIZE"), "regexp": r'^DGSIZE,(T\d+),(.+)$', "scope": "NMONDGSIZE"},
                {"action": self.genc1("NMONFILE"), "regexp": r'^FILE,File .*?,(.+)$', "scope": "NMONFILE"},
                {"action": self.genv1("NMONFILE"), "regexp": r'^FILE,(T\d+),(.+)$', "scope": "NMONFILE"},
                {"action": self.genc1("NMONIOADAPT"), "regexp": r'^IOADAPT,Disk .*?,(.+)$', "scope": "NMONIOADAPT"},
                {"action": self.genv1("NMONIOADAPT"), "regexp": r'^IOADAPT,(T\d+),(.+)$', "scope": "NMONIOADAPT"},
                {"action": self.genc1("NMONJFSFILE"), "regexp": r'^JFSFILE,JFS .*?,(.+)$', "scope": "NMONJFSFILE"},
                {"action": self.genv1("NMONJFSFILE"), "regexp": r'^JFSFILE,(T\d+),(.+)$', "scope": "NMONJFSFILE"},
                {"action": self.genc1("NMONJFSINODE"), "regexp": r'^JFSINODE,JFS .*?,(.+)$', "scope": "NMONJFSINODE"},
                {"action": self.genv1("NMONJFSINODE"), "regexp": r'^JFSINODE,(T\d+),(.+)$', "scope": "NMONJFSINODE"},
                {"action": self.genc1("NMONLARGEPAGE"), "regexp": r'^LARGEPAGE,Large Page .*?,(.+)$', "scope": "NMONLARGEPAGE"},
                {"action": self.genv1("NMONLARGEPAGE"), "regexp": r'^LARGEPAGE,(T\d+),(.+)$', "scope": "NMONLARGEPAGE"},
                {"action": self.genc1("NMONLPAR"), "regexp": r'^LPAR,Logical Partition .*?,(.+)$', "scope": "NMONLPAR"},
                {"action": self.genc1("NMONLPAR"), "regexp": r'^LPAR,LPAR .*?,(.+)$', "scope": "NMONLPAR"},
                {"action": self.genv1("NMONLPAR"), "regexp": r'^LPAR,(T\d+),(.+)$', "scope": "NMONLPAR"},
                {"action": self.genc1("NMONMEM"), "regexp": r'^MEM,Memory.*?,(.+)$', "scope": "NMONMEM"},
                {"action": self.genv1("NMONMEM"), "regexp": r'^MEM,(T\d+),(.+)$', "scope": "NMONMEM"},
                {"action": self.genc1("NMONMEMNEW"), "regexp": r'^MEMNEW,Memory *New.*?,(.+)$', "scope": "NMONMEMNEW"},
                {"action": self.genv1("NMONMEMNEW"), "regexp": r'^MEMNEW,(T\d+),(.+)$', "scope": "NMONMEMNEW"},
                {"action": self.genc1("NMONMEMUSE"), "regexp": r'^MEMUSE,Memory *Use.*?,(.+)$', "scope": "NMONMEMUSE"},
                {"action": self.genv1("NMONMEMUSE"), "regexp": r'^MEMUSE,(T\d+),(.+)$', "scope": "NMONMEMUSE"},
                {"action": self.genc1("NMONNET"), "regexp": r'^NET,Network .*?,(.+)$', "scope": "NMONNET"},
                {"action": self.genv1("NMONNET"), "regexp": r'^NET,(T\d+),(.+)$', "scope": "NMONNET"},
                {"action": self.genc1("NMONNETERROR"), "regexp": r'^NETERROR,Network .*?,(.+)$', "scope": "NMONNETERROR"},
                {"action": self.genv1("NMONNETERROR"), "regexp": r'^NETERROR,(T\d+),(.+)$', "scope": "NMONNETERROR"},
                {"action": self.genc1("NMONNETPACKET"), "regexp": r'^NETPACKET,Network .*?,(.+)$', "scope": "NMONNETPACKET"},
                {"action": self.genv1("NMONNETPACKET"), "regexp": r'^NETPACKET,(T\d+),(.+)$', "scope": "NMONNETPACKET"},
                {"action": self.genc1("NMONNETSIZE"), "regexp": r'^NETSIZE,Network .*?,(.+)$', "scope": "NMONNETSIZE"},
                {"action": self.genv1("NMONNETSIZE"), "regexp": r'^NETSIZE,(T\d+),(.+)$', "scope": "NMONNETSIZE"},
                {"action": self.genc1("NMONNFSCLIV2"), "regexp": r'^NFSCLIV2,NFS Client .*?,(.+)$', "scope": "NMONNFSCLIV2"},
                {"action": self.genv1("NMONNFSCLIV2"), "regexp": r'^NFSCLIV2,(T\d+),(.+)$', "scope": "NMONNFSCLIV2"},
                {"action": self.genc1("NMONNFSCLIV3"), "regexp": r'^NFSCLIV3,NFS Client .*?,(.+)$', "scope": "NMONNFSCLIV3"},
                {"action": self.genv1("NMONNFSCLIV3"), "regexp": r'^NFSCLIV3,(T\d+),(.+)$', "scope": "NMONNFSCLIV3"},
                {"action": self.genc1("NMONNFSSVRV2"), "regexp": r'^NFSSVRV2,NFS Server .*?,(.+)$', "scope": "NMONNFSSVRV2"},
                {"action": self.genv1("NMONNFSSVRV2"), "regexp": r'^NFSSVRV2,(T\d+),(.+)$', "scope": "NMONNFSSVRV2"},
                {"action": self.genc1("NMONNFSSVRV3"), "regexp": r'^NFSSVRV3,NFS Server .*?,(.+)$', "scope": "NMONNFSSVRV3"},
                {"action": self.genv1("NMONNFSSVRV3"), "regexp": r'^NFSSVRV3,(T\d+),(.+)$', "scope": "NMONNFSSVRV3"},
                {"action": self.genc1("NMONPAGE"), "regexp": r'^PAGE,Paging .*?,(.+)$', "scope": "NMONPAGE"},
                {"action": self.genv1("NMONPAGE"), "regexp": r'^PAGE,(T\d+),(.+)$', "scope": "NMONPAGE"},
                {"action": self.genc1("NMONPOOLS"), "regexp": r'^POOLS,Multiple .*?,(.+)$', "scope": "NMONPOOLS"},
                {"action": self.genv1("NMONPOOLS"), "regexp": r'^POOLS,(T\d+),(.+)$', "scope": "NMONPOOLS"},
                {"action": self.genc1("NMONPROC"), "regexp": r'^PROC,Processes .*?,(.+)$', "scope": "NMONPROC"},
                {"action": self.genv1("NMONPROC"), "regexp": r'^PROC,(T\d+),(.+)$', "scope": "NMONPROC"},
                {"action": self.genc1("NMONPROCAIO"), "regexp": r'^PROCAIO,Asynchronous .*?,(.+)$', "scope": "NMONPROCAIO"},
                {"action": self.genv1("NMONPROCAIO"), "regexp": r'^PROCAIO,(T\d+),(.+)$', "scope": "NMONPROCAIO"},
                {"action": self.genc1("NMONVM"), "regexp": r'^VM,Paging .*?,(.+)$', "scope": "NMONVM"},
                {"action": self.genv1("NMONVM"), "regexp": r'^VM,(T\d+),(.+)$', "scope": "NMONVM"},
                {"action": self.top, "regexp": r'^TOP,.PID,Time,(.+)$', "scope": "NMONTOP"},
                {"action": self.topval, "regexp": r'^TOP,([0-9]+),(T\d+),(.+)$', "scope": "NMONTOP"},
                {"action": self.aaa, "regexp": r'^AAA,(.+?),(.+)$', "scope": "NMONAAA"},
            ]
        }
        super(UserObject, self).__init__(**object)

    def begin(self, a):
        def tof(x):
            try: r = float(x)
            except: r = float(0)
            if str(r) == 'inf': r = 0.0
            if str(r) == 'nan': r = 0.0
            return r
        a.tof = tof
        a.desc = dict()
        a.nmontimestamp = dict()
        a.month = dict(JAN='01', FEB='02', MAR='03', APR='04', MAY='05', JUN='06', JUL='07', AUG='08', SEP='09', OCT='10', NOV='11', DEC='12')

    def end(self, a):
        pass

    def gettimestamp(self, a, l, g, m):
        a.nmontimestamp[g(1)] = g(7) + a.month[g(6).upper()] + g(5) + g(2) + g(3) + g(4) + "000"

    def getcpuval(self, a, l, g, m):
        if "NMONCPU" not in a.desc: a.desc["NMONCPU"] = dict(timestamp='text', id='text', usr='real', sys='real', wait='real', idle='real', busy='real', cpus='real')
        cpuid = int(g(1)[3:])
        a.emit("NMONCPU", a.desc["NMONCPU"], dict(timestamp = a.nmontimestamp[g(2)], id = cpuid, usr = a.tof(g(3)), sys = a.tof(g(4)), wait = a.tof(g(5)), idle = a.tof(g(6)), busy = 0.0, cpus = 1.0))

    def getcpuall(self, a, l, g, m):
        if "NMONCPU" not in a.desc: a.desc["NMONCPU"] = dict(timestamp='text', id='text', usr='real', sys='real', wait='real', idle='real', busy='real', cpus='real')
        cpuid='ALL'
        a.emit("NMONCPU", a.desc["NMONCPU"], dict(timestamp = a.nmontimestamp[g(1)], id = cpuid, usr = a.tof(g(2)), sys = a.tof(g(3)), wait = a.tof(g(4)), idle = a.tof(g(5)), busy = a.tof(g(6)), cpus = a.tof(g(7))))

    def genc1(self, table):
        def f(a, l ,g, m):
            setattr(a, table.lower(), g(1).split(','))
            if table not in a.desc: a.desc[table] = dict(timestamp = 'text', id = 'text', value = 'real')
        return f

    def genv1(self, table):
        def f(a, l ,g, m):
            val=g(2).split(',')
            for i in range(len(val)): a.emit(table, a.desc[table], dict(timestamp = a.nmontimestamp[g(1)], id = getattr(a, table.lower())[i], value = a.tof(val[i])))
        return f

    def genc2(self, table):
        def f(a, l ,g, m):
            i = g(1) if g(1) else 0
            if not hasattr(a, table.lower()): setattr(a, table.lower(), {})
            getattr(a, table.lower())[i] = g(2).split(',')
            if table not in a.desc: a.desc[table] = dict(timestamp = 'text', id = 'text', value = 'real')
        return f

    def genv2(self, table):
        def f(a, l ,g, m):
            i = g(1) if g(1) else 0
            val = g(3).split(',')
            for j in range(len(val)): a.emit(table, a.desc[table], dict(timestamp = a.nmontimestamp[g(2)], id = getattr(a,table.lower())[i][j], value = a.tof(val[j])))
        return f

    def top(self, a, l, g, m):
        setattr(a, 'nmontop', g(1).split(','))
        a.desc['NMONTOP'] = dict(timestamp = 'text', process = 'text', id = 'text', value = 'text')

    def topval(self, a, l, g, m):
        val = g(3).split(',')
        for i in range(len(val)): a.emit('NMONTOP', a.desc['NMONTOP'], dict(timestamp = a.nmontimestamp[g(2)], process = g(1), id = getattr(a, 'nmontop')[i], value = val[i]))

    def aaa(self, a, l, g, m):
        if 'NMONAAA' not in a.desc: a.desc['NMONAAA'] = dict(id = 'text', value = 'text')
        a.emit('NMONAAA', a.desc['NMONAAA'], dict(id = g(1), value = g(2)))
