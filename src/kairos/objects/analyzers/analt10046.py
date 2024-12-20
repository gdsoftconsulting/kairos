class UserObject(dict):
    def __init__(self):
        object = {
            "type": "analyzer",
            "id": "ANALT10046",
            "begin": self.begin,
            "end": self.end,
            "rules": [
                {"action": self.flushparsing, "regexp": r"^END OF STMT", "scope": "TPARSING"},

            ],
            "contextrules": [
                {"action": self.getrequest, "regexp": r'^(.+)$', "context": "request", "scope": "TPARSING"},
                {"action": self.getbindnum, "regexp": r'^ Bind#(\d+)$', "context": "bind", "scope": "TBINDS"},
                {"action": self.getbindtype, "regexp": r'^  oacdty=(\d+) ', "context": "bindtype", "scope": "TBINDS"},
                {"action": self.getbindvalue, "regexp": r'^  value=(.+)$', "context": "bindvalue", "scope": "TBINDS"},
            ],
            "outcontextrules": [
                {"action": self.getopid, "regexp": r'^Oracle process number: (\d+)', "scope": "TPARSING"},
                {"action": self.getpid, "regexp": r'^Unix process pid: (\d+), image: (.+?)$', "scope": "TPARSING"},
                {"action": self.getsid, "regexp": r'^\*\*\* SESSION ID:\((.+?)\)', "scope": "TPARSING"},
                {"action": self.getclose, "regexp": r'^CLOSE #(\d+):c=(\d+),e=(\d+),dep=(\d+),type=(\d+),tim=(\d+)$', "scope": "TCLOSE"},
                {"action": self.getparsing, "regexp": r"^PARSING IN CURSOR #(\d+) len=(\d+) dep=(\d+) uid=(\d+) oct=(\d+) lid=(\d+) tim=(\d+) hv=(\d+) ad='(.+?)' sqlid='(.+?)'$", "scope": "TPARSING"},
                {"action": self.getexec, "regexp": r"^EXEC #(\d+):c=(\d+),e=(\d+),p=(\d+),cr=(\d+),cu=(\d+),mis=(\d+),r=(\d+),dep=(\d+),og=(\d+),plh=(\d+),tim=(\d+)$", "scope": "TEXEC"},
                {"action": self.getfetch, "regexp": r"^FETCH #(\d+):c=(\d+),e=(\d+),p=(\d+),cr=(\d+),cu=(\d+),mis=(\d+),r=(\d+),dep=(\d+),og=(\d+),plh=(\d+),tim=(\d+)$", "scope": "TFETCH"},
                {"action": self.getstat, "regexp": r"^STAT #(\d+) id=(\d+) cnt=(\d+) pid=(\d+) pos=(\d+) obj=(\d+) op='(.+?) \(cr=(\d+) pr=(\d+) pw=(\d+) str=(\d+) time=(\d+) (\w+)", "scope": "TSTAT"},
                {"action": self.getwait, "regexp": r"^WAIT #(\d+): nam='(.+?)' ela= (\d+) .+tim=(\d+)", "scope": "TWAIT"},
                {"action": self.geterror, "regexp": r"^ERROR #(\d+):err=(\d+) tim=(\d+)", "scope": "TERROR"},
                {"action": self.getbinds, "regexp": r"^BINDS #(\d+):", "scope": "TBINDS"},
                {"action": self.getxctend, "regexp": r"^XCTEND rlb=(\d+), rd_only=(\d+), tim=(\d+)$", "scope": "TXCTEND"},
            ]
        }
        super(UserObject, self).__init__(**object)

    def begin(self, a):
        pass

    def end(self, a):
        pass
    
    def getopid(self, a, l, g, m):
        a.opid = int(g(1))
    
    def getpid(self, a, l, g, m):
        a.pid = int(g(1))
        a.image = g(2)
    
    def getsid(self, a, l, g, m):
        a.sid = g(1)

    def getclose(self, a, l, g, m):
        desc = dict(cid='text',c='bigint',e='bigint',dep='int',type='int',tim='bigint')
        cid = str(g(1))
        c = int(g(2))
        e = int(g(3))
        dep = int(g(4))
        type = int(g(5))
        tim = int(g(6))
        a.emit('TCLOSE', desc, dict(cid=cid,c=c,e=e,dep=dep,type=type,tim=tim))

    def getparsing(self, a, l, g, m):
        desc = dict(cid='text',opid='int',pid='int',image='text',sid='text',dep='int',uid='int',tim='bigint',hv='bigint',ad='text',sqlid='text',request='text')
        cid = str(g(1))
        dep = int(g(3))
        uid = int(g(4))
        tim = int(g(7))
        hv = int(g(8))
        ad = str(g(9))
        sqlid = str(g(10))
        a.desc = desc
        a.data = dict(cid=cid,opid=a.opid,pid=a.pid,image=a.image,sid=a.sid,dep=dep,uid=uid,tim=tim,hv=hv,ad=ad,sqlid=sqlid)
        a.count = 0
        a.setContext('request')

    def getrequest(self, a, l, g, m):
        a.request = a.request + str(g(1)) if a.count > 0 else ''
        a.count += 1

    def flushparsing(self, a, l, g, m):
        a.trace('DEBUG ANALT10046 request: ' +str(a.request))
        a.data['request'] = a.request
        a.emit('TPARSING', a.desc, a.data)
        a.setContext('')

    def getbinds(self, a, l, g, m):
        desc = dict(cid='text',id='int',type='text',value='text')
        cid = str(g(1))
        a.desc = desc
        a.data = dict(cid=cid)
        a.trace('DEBUG ANALT10046 cid: ' + cid)
        a.setContext('bind')

    def getbindnum(self, a, l, g, m):
        id = int(g(1))
        a.data['id'] = id
        a.trace('DEBUG ANALT10046 id: ' + str(id))
        a.setContext('bindtype')

    def getbindtype(self, a, l, g, m):
        type = str(g(1))
        a.data['type'] = type
        a.trace('DEBUG ANALT10046 type: ' + type)
        a.setContext('bindvalue')

    def getbindvalue(self, a, l, g, m):
        value = str(g(1))
        a.data['value'] = value
        a.trace('DEBUG ANALT10046 value: ' + value)
        a.emit('TBINDS', a.desc, a.data)
        a.setContext('')

    def getexec(self, a, l, g, m):
        desc = dict(cid='text',c='bigint',e='bigint',p='bigint',cr='bigint',cu='bigint',mis='int',r='bigint',dep='int',og='bigint',plh='bigint',tim='bigint')
        cid = str(g(1))
        c = int(g(2))
        e = int(g(3))
        p = int(g(4))
        cr = int(g(5))
        cu = int(g(6))
        mis = int(g(7))
        r = int(g(8))
        dep = int(g(9))
        og = int(g(10))
        plh = int(g(11))
        tim = int(g(12))
        a.emit('TEXEC', desc, dict(cid=cid,c=c,e=e,p=p,cr=cr,cu=cu,mis=mis,r=r,dep=dep,og=og,plh=plh,tim=tim))

    def getfetch(self, a, l, g, m):
        desc = dict(cid='text',c='bigint',e='bigint',p='bigint',cr='bigint',cu='bigint',mis='int',r='bigint',dep='int',og='bigint',plh='bigint',tim='bigint')
        cid = str(g(1))
        c = int(g(2))
        e = int(g(3))
        p = int(g(4))
        cr = int(g(5))
        cu = int(g(6))
        mis = int(g(7))
        r = int(g(8))
        dep = int(g(9))
        og = int(g(10))
        plh = int(g(11))
        tim = int(g(12))
        a.emit('TFETCH', desc, dict(cid=cid,c=c,e=e,p=p,cr=cr,cu=cu,mis=mis,r=r,dep=dep,og=og,plh=plh,tim=tim))

    def getstat(self, a, l, g, m):
        desc = dict(cid='text',id='int',cnt='int',pid='int',pos='int',obj='bigint',op='text',cr='bigint',pr='bigint',pw='bigint',st='int',time='bigint',unit='text')
        cid = str(g(1))
        id = int(g(2))
        cnt = int(g(3))
        pid = int(g(4))
        pos = int(g(5))
        obj = int(g(6))
        op = str(g(7))
        cr = int(g(8))
        pr = int(g(9))
        pw = int(g(10))
        st = int(g(11))
        time = int(g(12))
        unit = str(g(13))
        a.emit('TSTAT', desc, dict(cid=cid,id=id,cnt=cnt,pid=pid,pos=pos,obj=obj,op=op,cr=cr,pr=pr,pw=pw,st=st,time=time,unit=unit))

    def getwait(self, a, l, g, m):
        desc = dict(cid='text',nam='text',ela='bigint',tim='bigint')
        cid = str(g(1))
        nam = str(g(2))
        ela = int(g(3))
        tim = int(g(4))
        a.emit('TWAIT', desc, dict(cid=cid,nam=nam,ela=ela,tim=tim))

    def geterror(self, a, l, g, m):
        desc = dict(cid='text',err='int',tim='bigint')
        cid = str(g(1))
        err = int(g(2))
        tim = int(g(3))
        a.emit('TERROR', desc, dict(cid=cid,err=err,tim=tim))
        
    def getxctend(self, a, l, g, m):
        desc = dict(rlbk='int',rd_only='int',tim='bigint')
        rlbk = int(g(1))
        rd_only = int(g(2))
        tim = int(g(3))
        a.emit('TXCTEND', desc, dict(rlbk=rlbk,rd_only=rd_only,tim=tim))