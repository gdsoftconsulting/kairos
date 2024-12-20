class UserObject(dict):
    def __init__(self):
        object = {
            "type": "analyzer",
            "id": "ANALAWRRACHTML",
            "content": "xml",
            "begin": self.begin,
            "end": self.end,
            "rules": [
                {"action": self.ah3, "regexp": r'', "tag": 'h3'},
                {"action": self.atable, "regexp": r'', "tag": 'table'},
                {"action": self.atr, "regexp": r'', "tag": 'tr'},
                {"action": self.athd, "regexp": r'', "tag": '(th|td)'}
            ],
            "contextrules": [
                {"action": self.atdgetd, "regexp": r'', "tag": 'td', "context": "tdgetd"},
            ],
            "outcontextrules": [
                {"action": self.genstate('tdgetd'), "regexp": r'Complete List of SQL Text', "tag": 'h3', "scope": "DBORARACREQ"},
                {"action": self.genstate('tdgetd'), "regexp": r'Foreground Wait Classes$', "tag": 'h3', "scope": "DBORARACFWC"},
                {"action": self.genstate('tdgetd'), "regexp": r'Global Cache Efficiency Percentages', "tag": 'h3', "scope": "DBORARACGCEP"},
                {"action": self.genstate('tdgetd'), "regexp": r'Global Cache Transfer Stats', "tag": 'h3', "scope": "DBORARACGCTS"},
                {"action": self.genstate('tdgetd'), "regexp": r'Global Messaging Statistics \(Global\)', "tag": 'h3', "scope": "DBORARACSTA"},
                {"action": self.genstate('tdgetd'), "regexp": r'OS Statistics By Instance', "tag": 'h3', "scope": "DBORARACOSS"},
                {"action": self.genstate('tdgetd'), "regexp": r'Ping Statistics', "tag": 'h3', "scope": "DBORARACPING"},
                {"action": self.genstate('tdgetd'), "regexp": r'Report Summary', "tag": 'h3', "scope": "DBORARACCSIZE"},
                {"action": self.genstate('tdgetd'), "regexp": r'Segment Statistics \(Global\)', "tag": 'h3', "scope": "DBORARACSEG"},
                {"action": self.genstate('tdgetd'), "regexp": r'SQL ordered by Elapsed Time .Global.', "tag": 'h3', "scope": "DBORARACSQE"},
                {"action": self.genstate('tdgetd'), "regexp": r'SQL ordered by CPU Time .Global.', "tag": 'h3', "scope": "DBORARACSQC"},
                {"action": self.genstate('tdgetd'), "regexp": r'SQL ordered by User I/O Time .Global.', "tag": 'h3', "scope": "DBORARACSQI"},
                {"action": self.genstate('tdgetd'), "regexp": r'SQL ordered by Gets .Global.', "tag": 'h3', "scope": "DBORARACSQG"},
                {"action": self.genstate('tdgetd'), "regexp": r'SQL ordered by Reads .Global.', "tag": 'h3', "scope": "DBORARACSQR"},
                {"action": self.genstate('tdgetd'), "regexp": r'SQL ordered by UnOptimized Read Requests .Global.', "tag": 'h3', "scope": "DBORARACSQU"},
                {"action": self.genstate('tdgetd'), "regexp": r'SQL ordered by Executions .Global.', "tag": 'h3', "scope": "DBORARACSQX"},
                {"action": self.genstate('tdgetd'), "regexp": r'SQL ordered by Cluster Wait Time .Global.', "tag": 'h3', "scope": "DBORARACSQW"},
                {"action": self.genstate('tdgetd'), "regexp": r'SysStat and Global Messaging  - RAC$', "tag": 'h3', "scope": "DBORARACGALPGM"},
                {"action": self.genstate('tdgetd'), "regexp": r'System Statistics$', "tag": 'h3', "scope": "DBORARACGALPSS"},
                {"action": self.genstate('tdgetd'), "regexp": r'System Statistics \(Global\)', "tag": 'h3', "scope": "DBORARACSTA"},
                {"action": self.genstate('tdgetd'), "regexp": r'System Statistics \(Absolute Values\)', "tag": 'h3', "scope": "DBORARACSTAA"},
                {"action": self.genstate('tdgetd'), "regexp": r'Time Model$', "tag": 'h3', "scope": "DBORARACTM"},
                {"action": self.genstate('tdgetd'), "regexp": r'Top Timed Background Events', "tag": 'h3', "scope": "DBORARACTTBE"},
                {"action": self.genstate('tdgetd'), "regexp": r'Top Timed Events', "tag": 'h3', "scope": "DBORARACTTE"},
                {"action": self.genstate('tdgetd'), "regexp": r'Top Timed Foreground Events', "tag": 'h3', "scope": "DBORARACTTFE"},
                {"action": self.genstate('tdgetd'), "regexp": r'Snapshot Ids', "tag": 'th'},
                {"action": self.genstate('tdgetd'), "regexp": r'Begin Snap Time', "tag": 'th'},
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
        tos=lambda x: x.replace(u'\xa0','')
        for x in sorted(a.collected.keys(),reverse=True):
            if x=='zz9':
                a.dur = {}
                inum = 0
                for y in a.collected[x]: a.dur[inum] = tof(y[11]) * 60

            if x=='zz8':
                a.date = {}
                a.version = {}
                desc = dict(timestamp='text',inum='text',instance='text',host='text',avgelapsed='real',elapsed='int',avgdbtime='real',avgactivesess='real')
                stack = []
                stack = []
                for y in a.collected[x]:
                    inum = int(y[0])
                    instance = y[1]
                    host = y[2]
                    what = y[5]
                    year = str('20' + what[7:9])
                    month = a.month[str(what[3:6])]
                    day = str(what[0:2])
                    hour = str(what[10:12])
                    min = str(what[13:15])
                    a.date[inum] = year+month+day+hour+min+'00000'
                    a.date[0] = a.date[inum]
                    a.dur[inum] = tof(y[7])*60
                    a.version[inum] = y[6]
                    dbtime = tof(y[8]) * 60 / a.dur[inum]
                    avgactivesess = tof(y[10])
                    stack.append(dict(timestamp=a.date[inum],inum=str(inum),instance=instance,host=host,avgelapsed=a.dur[inum],elapsed=int(a.dur[inum]),avgdbtime=dbtime,avgactivesess=avgactivesess))
                if 'DBORARACMISC' in a.scope: a.emit('DBORARACMISC', desc, stack)

            if x=='Report Summary':
                desc = dict(timestamp='text',inum='text',dbcache='real',sharedpool='real',largepool='real',javapool='real',streampool='real',pgatarget='real',logbuffer='real')
                stack = []
                for y in a.collected[x]:
                    try: inum = int(y[0])
                    except: continue
                    dbcache = tof(y[5])
                    sharedpool = tof(y[7])
                    largepool = tof(y[9])
                    javapool = tof(y[11])
                    streampool = tof(y[13])
                    pgatarget = tof(y[15])
                    logbuffer = tof(y[17])
                    stack.append(dict(timestamp=a.date[inum],inum=str(inum),dbcache=dbcache,sharedpool=sharedpool,largepool=largepool,javapool=javapool,streampool=streampool,pgatarget=pgatarget,logbuffer=logbuffer))
                a.emit('DBORARACCSIZE', desc, stack)

            if x=='OS Statistics By Instance':
                desc = dict(timestamp='text',inum='text',numcpus='real',cpucores='real',loadend='real',busyp='real',usrp='real',sysp='real',wiop='real',idlp='real',busytime='real',idletime='real',totaltime='real',memory='real')
                stack = []
                for y in a.collected[x]:
                    try: inum = int(y[0])
                    except: continue
                    numcpus = tof(y[1])
                    cpucores = tof(y[2])
                    loadend = tof(y[5])
                    busyp = tof(y[6])
                    usrp = tof(y[7])
                    sysp = tof(y[8])
                    wiop = tof(y[9])
                    idlp = tof(y[10])
                    busytime = tof(y[11]) / a.dur[inum]
                    idletime = tof(y[12]) / a.dur[inum]
                    totaltime = tof(y[13]) / a.dur[inum]
                    memory = tof(y[14])
                    stack.append(dict(timestamp=a.date[inum],inum=str(inum),numcpus=numcpus,cpucores=cpucores,loadend=loadend,busyp=busyp,usrp=usrp,sysp=sysp,wiop=wiop,idlp=idlp,busytime=busytime,idletime=idletime,totaltime=totaltime,memory=memory))
                a.emit('DBORARACOSS', desc, stack)

            if x=='Time Model':
                desc = dict(timestamp='text',inum='text',dbtime='real',dbcpu='real',sqlexecela='real',parseela='real',hardparseela='real',plsqlela='real',javaela='real',bgtime='real',bgcpu='real')
                stack = []
                for y in a.collected[x]:
                    try: inum = int(y[0])
                    except: continue
                    dbtime = tof(y[1]) / a.dur[inum]
                    dbcpu = tof(y[2]) / a.dur[inum]
                    sqlexecela = tof(y[3]) / a.dur[inum]
                    parseela = tof(y[4]) / a.dur[inum]
                    hardparseela = tof(y[5]) / a.dur[inum]
                    plsqlela = tof(y[6]) / a.dur[inum]
                    javaela = tof(y[7]) / a.dur[inum]
                    bgtime = tof(y[8]) / a.dur[inum]
                    bgcpu = tof(y[9]) / a.dur[inum]
                    stack.append(dict(timestamp=a.date[inum],inum=str(inum),dbtime=dbtime,dbcpu=dbcpu,sqlexecela=sqlexecela,parseela=parseela,hardparseela=hardparseela,plsqlela=plsqlela,javaela=javaela,bgtime=bgtime,bgcpu=bgcpu))
                a.emit('DBORARACTM', desc, stack)

            if x=='Foreground Wait Classes':
                desc = dict(timestamp='text',inum='text',userio='real',sysio='real',other='real',applic='real',commits='real',network='real',concurcy='real',config='real',cluster='real',dbcpu='real',dbtime='real')
                stack = []
                for y in a.collected[x]:
                    try: inum = int(y[0])
                    except: continue
                    userio = tof(y[1]) / a.dur[inum]
                    sysio = tof(y[2]) / a.dur[inum]
                    other = tof(y[3]) / a.dur[inum]
                    applic = tof(y[4]) / a.dur[inum]
                    commits = tof(y[5]) / a.dur[inum]
                    network = tof(y[6]) / a.dur[inum]
                    concurcy = tof(y[7]) / a.dur[inum]
                    config = tof(y[8]) / a.dur[inum]
                    cluster = tof(y[9]) / a.dur[inum]
                    dbcpu = tof(y[10]) / a.dur[inum]
                    dbtime = tof(y[11]) / a.dur[inum]
                    stack.append(dict(timestamp=a.date[inum],inum=str(inum),dbtime=dbtime,dbcpu=dbcpu,userio=userio,sysio=sysio,other=other,applic=applic,commits=commits,network=network,concurcy=concurcy,config=config,cluster=cluster))
                a.emit('DBORARACFWC', desc, stack)


            if x in ['Top Timed Events','Top Timed Foreground Events','Top Timed Background Events']:
                collection = 'DBORARACTTE' if x=='Top Timed Events' else 'DBORARACTTFE' if x=='Top Timed Foreground Events' else 'DBORARACTTBE'
                desc = dict(timestamp='text',inum='text',klass='text',event='text',waits='real',ptimeouts='real',timewaited='real',pdbtime='real')
                stack = []
                for y in a.collected[x]:
                    if len(y)!=13: continue
                    try:
                        inum = int(0 if y[0]=='*' else y[0])
                        a.inum = inum
                    except: inum = a.inum
                    klass = tos(y[1])
                    event = y[2]
                    try: waits = tof(y[3])/a.dur[inum]
                    except: waits = 0.0
                    try: ptimeouts = tof(y[4])
                    except: ptimeouts = 0.0
                    timewaited = tof(y[5])/a.dur[inum]
                    pdbtime = tof(y[7])
                    stack.append(dict(timestamp=a.date[inum],inum=str(inum),klass=klass,event=event,waits=waits,ptimeouts=ptimeouts,timewaited=timewaited,pdbtime=pdbtime))
                a.emit(collection, desc, stack)

            if x=='System Statistics':
                desc = dict(timestamp='text',inum='text',logicalreads='real',physicalreads='real',physicalwrites='real',redosizek='real',blockchanges='real',usercalls='real',execs='real',parses='real',logons='real',txns='real')
                stack = []
                for y in a.collected[x]:
                    try: inum = int(y[0])
                    except: continue
                    logicalreads = tof(y[1]) / a.dur[inum]
                    physicalreads = tof(y[2]) / a.dur[inum]
                    physicalwrites = tof(y[3]) / a.dur[inum]
                    redosizek = tof(y[4]) / a.dur[inum]
                    blockchanges = tof(y[5]) / a.dur[inum]
                    usercalls = tof(y[6]) / a.dur[inum]
                    execs = tof(y[7]) / a.dur[inum]
                    parses = tof(y[8]) / a.dur[inum]
                    logons = tof(y[9]) / a.dur[inum]
                    txns = tof(y[10]) / a.dur[inum]
                    stack.append(dict(timestamp=a.date[inum],inum=str(inum),logicalreads=logicalreads,physicalreads=physicalreads,physicalwrites=physicalwrites,redosizek=redosizek,blockchanges=blockchanges,usercalls=usercalls,execs=execs,parses=parses,logons=logons,txns=txns))
                a.emit('DBORARACGALPSS', desc, stack)

            if x=='SysStat and Global Messaging  - RAC':
                desc = dict(timestamp='text',inum='text',brgcct='real',brgccr='real',bsgcct='real',bsgccr='real',cpugc='real',cpuipc='real',mgcsr='real',mgesr='real',mgcss='real',mgess='real',msd='real',msi='real',gcbl='real',gccrf='real')
                stack = []
                for y in a.collected[x]:
                    try: inum = int(y[0])
                    except: continue
                    brgcct = tof(y[1]) / a.dur[inum]
                    brgccr = tof(y[2]) / a.dur[inum]
                    bsgcct = tof(y[3]) / a.dur[inum]
                    bsgccr = tof(y[4]) / a.dur[inum]
                    cpugc = tof(y[5]) / a.dur[inum]
                    cpuipc = tof(y[6]) / a.dur[inum]
                    mgcsr = tof(y[7]) / a.dur[inum]
                    mgesr = tof(y[8]) / a.dur[inum]
                    mgcss = tof(y[9]) / a.dur[inum]
                    mgess = tof(y[10]) / a.dur[inum]
                    msd = tof(y[11]) / a.dur[inum]
                    msi = tof(y[12]) / a.dur[inum]
                    gcbl = tof(y[13]) / a.dur[inum]
                    gccrf = tof(y[14]) / a.dur[inum]
                    stack.append(dict(timestamp=a.date[inum],inum=str(inum),brgcct=brgcct,brgccr=brgccr,bsgcct=bsgcct,bsgccr=bsgccr,cpugc=cpugc,cpuipc=cpuipc,mgcsr=mgcsr,mgesr=mgesr,mgcss=mgcss,mgess=mgess,msd=msd,msi=msi,gcbl=gcbl,gccrf=gccrf))
                a.emit('DBORARACGALPGM', desc, stack)

            if x=='Global Cache Efficiency Percentages':
                desc = dict(timestamp='text',inum='text',plocal='real',premote='real',pdisk='real')
                stack = []
                for y in a.collected[x]:
                    try: inum = int(y[0])
                    except: continue
                    plocal = tof(y[1])
                    premote = tof(y[2])
                    pdisk = tof(y[3])
                    stack.append(dict(timestamp=a.date[inum],inum=str(inum),plocal=plocal,premote=premote,pdisk=pdisk))
                a.emit('DBORARACGCEP', desc, stack)

            if x=='Global Cache Transfer Stats':
                desc = dict(timestamp='text',dest='text',src='text',bclass='text',crblocks='real',crimm='real',crbusy='real',crcngst='real',cublocks='real',cuimm='real',cubusy='real',cucngst='real',cravgimm='real',cravgbusy='real',cravgcngst='real',cuavgimm='real',cuavgbusy='real',cuavgcngst='real')
                stack = []
                for y in a.collected[x]:
                    a.dest = int(tof(y[0])) if tof(y[0]) else a.dest
                    src = y[1]
                    bclass = y[2]
                    crblocks = tof(y[3]) / a.dur[a.dest]
                    crimm = tof(y[4]) * crblocks
                    crbusy = tof(y[5]) * crblocks
                    crcngst = tof(y[6]) * crblocks
                    cublocks = tof(y[7]) / a.dur[a.dest]
                    cuimm = tof(y[8]) * cublocks
                    cubusy = tof(y[9]) * cublocks
                    cucngst = tof(y[10]) * cublocks
                    cravgimm = tof(y[12])
                    cravgbusy = tof(y[13])
                    cravgcngst = tof(y[14])
                    cuavgimm = tof(y[16])
                    cuavgbusy = tof(y[17])
                    cuavgcngst = tof(y[18])
                    stack.append(dict(timestamp=a.date[a.dest],dest=str(a.dest),src=src,bclass=bclass,crblocks=crblocks,crimm=crimm,crbusy=crbusy,crcngst=crcngst,cublocks=cublocks,cuimm=cuimm,cubusy=cubusy,cucngst=cucngst,cravgimm=cravgimm,cravgbusy=cravgbusy,cravgcngst=cravgcngst,cuavgimm=cuavgimm,cuavgbusy=cuavgbusy,cuavgcngst=cuavgcngst))
                a.emit('DBORARACGCTS', desc, stack)

            if x in ['System Statistics (Global)','Global Messaging Statistics (Global)']:
                desc = dict(timestamp='text',statistic='text',value='real')
                stack = []
                for y in a.collected[x]:
                    statistic = y[0]
                    value = tof(y[1]) / a.dur[0]
                    stack.append(dict(timestamp=a.date[0],statistic=statistic,value=value))
                a.emit('DBORARACSTA', desc, stack)

            if x in ['System Statistics (Absolute Values)']:
                desc = dict(timestamp='text',inum='text',statistic='text',value='real')
                stack = []
                for y in a.collected[x]:
                    try: inum = int(y[0])
                    except: continue
                    statistic = 'sessions'
                    value = tof(y[2])
                    stack.append(dict(timestamp=a.date[inum],inum=str(inum),statistic=statistic,value=value))
                    statistic = 'open cursors'
                    value = tof(y[4])
                    stack.append(dict(timestamp=a.date[inum],inum=str(inum),statistic=statistic,value=value))
                    statistic = 'session cached cursors'
                    value = tof(y[6])
                    stack.append(dict(timestamp=a.date[inum],inum=str(inum),statistic=statistic,value=value))
                a.emit('DBORARACSTAA', desc, stack)

            if x in ['Segment Statistics (Global)']:
                desc = dict(timestamp='text',statistic='text',owner='text',tablespace='text',object='text',subobject='text',objtype='text',value='real',ptotal='real',pcapture='real')
                stack = []
                for y in a.collected[x]:
                    if y[0]: a.statistic = y[0]
                    owner = y[1]
                    tablespace = y[2]
                    object = y[3]
                    subobject = tos(y[4])
                    objtype = y[5]
                    value = tof(y[6]) / a.dur[0]
                    try: ptotal = tof(y[7])
                    except: ptotal = 0.0
                    pcapture = tof(y[8])
                    stack.append(dict(timestamp=a.date[0],statistic=a.statistic,owner=owner,tablespace=tablespace,object=object,subobject=subobject,objtype=objtype,value=value,ptotal=ptotal,pcapture=pcapture))
                a.emit('DBORARACSEG', desc, stack)

            if x=='Ping Statistics':
                desc = dict(timestamp='text',inum='text',dest='text',pc500='real',avgtp500='real',pc8k='real',avgtp8k='real')
                stack = []
                for y in a.collected[x]:
                    try:
                        inum = int(y[0])
                        a.inum = inum
                    except: inum = a.inum
                    dest = int(y[1])
                    pc500 = tof(y[2]) / a.dur[inum]
                    avgtp500 = tof(y[4])
                    pc8k = tof(y[6]) / a.dur[inum]
                    avgtp8k = tof(y[8])
                    stack.append(dict(timestamp=a.date[inum],inum=str(inum),dest=str(dest),pc500=pc500,avgtp500=avgtp500,pc8k=pc8k,avgtp8k=avgtp8k))
                a.emit('DBORARACPING', desc, stack)

            if x=='Complete List of SQL Text':
                desc = dict(sqlid='text',module='text',request='text')
                stack = []
                for y in a.collected[x]:
                    sqlid = y[0]
                    request = toc(y[1])
                    module = a.sqlid[sqlid] if sqlid in a.sqlid else ''
                    stack.append(dict(sqlid=sqlid,module=module,request=request))
                a.emit('DBORARACREQ', desc, stack)

            if x in ['SQL ordered by Elapsed Time (Global)','SQL ordered by CPU Time (Global)','SQL ordered by User I/O Time (Global)','SQL ordered by Gets (Global)','SQL ordered by Reads (Global)','SQL ordered by UnOptimized Read Requests (Global)','SQL ordered by Executions (Global)','SQL ordered by Cluster Wait Time (Global)']:
                collection = 'DBORARACSQE' if x=='SQL ordered by Elapsed Time (Global)' else 'DBORARACSQC' if x=='SQL ordered by CPU Time (Global)' else 'DBORARACSQI' if x=='SQL ordered by User I/O Time (Global)' else 'DBORARACSQG' if x=='SQL ordered by Gets (Global)' else 'DBORARACSQR' if x=='SQL ordered by Reads (Global)' else 'DBORARACSQU' if x=='SQL ordered by UnOptimized Read Requests (Global)' else 'DBORARACSQX' if x=='SQL ordered by Executions (Global)' else 'DBORARACSQW' if x=='SQL ordered by Cluster Wait Time (Global)' else 'ERROR'
                desc = dict(timestamp='text',sqlid='text',elapsed='real',cpu='real',iowait='real',gets='real',reads='real',rows='real',cluster='real',execs='real')
                if x=='SQL ordered by Elapsed Time (Global)': (ie,ic,ii,ig,ir,iy,iz,ix) = (1,2,3,4,5,6,7,8)
                if x=='SQL ordered by CPU Time (Global)': (ie,ic,ii,ig,ir,iy,iz,ix) = (2,1,3,4,5,6,7,8)
                if x=='SQL ordered by User I/O Time (Global)': (ie,ic,ii,ig,ir,iy,iz,ix) = (2,3,1,4,5,6,7,8)
                if x=='SQL ordered by Gets (Global)': (ie,ic,ii,ig,ir,iy,iz,ix) = (3,4,5,1,2,6,7,8)
                if x=='SQL ordered by Reads (Global)': (ie,ic,ii,ig,ir,iy,iz,ix) = (3,4,5,2,1,6,7,8)
                if x=='SQL ordered by UnOptimized Read Requests (Global)': (ie,ic,ii,ig,ir,iy,iz,ix) = (3,4,5,1,2,6,7,8)
                if x=='SQL ordered by Executions (Global)': (ie,ic,ii,ig,ir,iy,iz,ix) = (2,3,4,5,6,7,8,1)
                if x=='SQL ordered by Cluster Wait Time (Global)': (ie,ic,ii,ig,ir,iy,iz,ix) = (2,3,4,5,6,7,1,8)
                stack = []
                for y in a.collected[x]:
                    if len(y) < 9: continue
                    sqlid = y[0]
                    elapsed = tof(y[ie]) / a.dur[0]
                    cpu = tof(y[ic]) / a.dur[0]
                    iowait = tof(y[ii]) / a.dur[0]
                    gets = tof(y[ig]) / a.dur[0]
                    reads = tof(y[ir]) / a.dur[0]
                    rows = tof(y[iy]) / a.dur[0]
                    cluster = tof(y[iz]) / a.dur[0]
                    execs = tof(y[ix]) / a.dur[0]
                    stack.append(dict(timestamp=a.date[0],sqlid=sqlid,elapsed=elapsed,cpu=cpu,iowait=iowait,gets=gets,reads=reads,rows=rows,cluster=cluster,execs=execs))
                a.emit(collection, desc, stack)

    def ah3(self, a, l, g, m):
        context = ''
        a.setContext(context)
        if len(a.row): a.tab.append(a.row)
        a.row = {}

    def atable(self, a, l, g, m):
        context = ''
        if a.reinit: a.setContext(context)
        if len(a.scope) < 3:
            if a.scope.issubset({'DBORARACMISC'}) and 'zz9' in a.collected and 'zz8' in a.collected: a.setContext('BREAK')
            if a.scope.issubset({'DBORARACCSIZE'}) and 'Report Summary' in a.collected and len(a.collected['Report Summary']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACOSS'}) and 'OS Statistics By Instance' in a.collected and len(a.collected['OS Statistics By Instance']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACTM'}) and 'Time Model' in a.collected and len(a.collected['Time Model']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACFWC'}) and 'Foreground Wait Classes' in a.collected and len(a.collected['Foreground Wait Classes']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACTTE'}) and 'Top Timed Events' in a.collected and len(a.collected['Top Timed Events']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACTTFE'}) and 'Top Timed Foreground Events' in a.collected and len(a.collected['Top Timed Foreground Events']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACTTBE'}) and 'Top Timed Background Events' in a.collected and len(a.collected['Top Timed Background Events']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACGALPSS'}) and 'System Statistics' in a.collected and len(a.collected['System Statistics']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACGALPGM'}) and 'SysStat and Global Messaging  - RAC' in a.collected and len(a.collected['SysStat and Global Messaging  - RAC']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACGCEP'}) and 'Global Cache Efficiency Percentages' in a.collected and len(a.collected['Global Cache Efficiency Percentages']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACGCTS'}) and 'Global Cache Transfer Stats' in a.collected and len(a.collected['Global Cache Transfer Stats']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACSTA'}) and 'Global Messaging Statistics (Global)' in a.collected and len(a.collected['Global Messaging Statistics (Global)']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACSTAA'}) and 'System Statistics (Absolute Values)' in a.collected and len(a.collected['System Statistics (Absolute Values)']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACSEG'}) and 'Segment Statistics (Global)' in a.collected and len(a.collected['Segment Statistics (Global)']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACPING'}) and 'Ping Statistics' in a.collected and len(a.collected['Ping Statistics']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACREQ'}) and 'Complete List of SQL Text' in a.collected and len(a.collected['Complete List of SQL Text']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACSQE'}) and 'SQL ordered by Elapsed Time (Global)' in a.collected and len(a.collected['SQL ordered by Elapsed Time (Global)']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACSQC'}) and 'SQL ordered by CPU Time (Global)' in a.collected and len(a.collected['SQL ordered by CPU Time (Global)']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACSQI'}) and 'SQL ordered by User I/O Time (Global)' in a.collected and len(a.collected['SQL ordered by User I/O Time (Global)']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACSQG'}) and 'SQL ordered by Gets (Global)' in a.collected and len(a.collected['SQL ordered by Gets (Global)']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACSQR'}) and 'SQL ordered by Reads (Global)' in a.collected and len(a.collected['SQL ordered by Reads (Global)']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACSQU'}) and 'SQL ordered by UnOptimized Read Requests (Global)' in a.collected and len(a.collected['SQL ordered by UnOptimized Read Requests (Global)']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACSQX'}) and 'SQL ordered by Executions (Global)' in a.collected and len(a.collected['SQL ordered by Executions (Global)']): a.setContext('BREAK')
            if a.scope.issubset({'DBORARACSQW'}) and 'SQL ordered by Cluster Wait Time (Global)' in a.collected and len(a.collected['SQL ordered by Cluster Wait Time (Global)']): a.setContext('BREAK')
        if len(a.row): a.tab.append(a.row)
        a.row = {}
        a.collector = {}

    def athget(self, a, l, g, m):
        if 0 not in a.collector: a.collector[0] = ''
        a.collector[a.cpt]=a.lxmltext(l)

    def atdget(self, a, l, g, m):
        if a.cpt in a.collector: a.row[a.collector[a.cpt]]=a.lxmltext(l)

    def atdgetd(self, a, l, g, m):
        a.row[a.cpt] = a.lxmltext(l)

    def atr(self, a, l, g, m):
        a.reinit = True
        a.cpt = -1
        if hasattr(a,'collector') and len(a.collector): a.setContext('td'+a.context[2:])
        if len(a.row): a.tab.append(a.row)
        a.row = {}

    def athd(self, a, l, g, m):
        a.cpt+=1

    def genstate(self, c):
        def f(a, l ,g, m):
            a.reinit = False
            a.setContext(c)
            a.tab = []
            k = a.lxmltext(l)
            if k == 'Snapshot Ids': k = 'zz9'
            if k == 'Begin Snap Time': k = 'zz8'
            a.collected[k] = a.tab
        return f
