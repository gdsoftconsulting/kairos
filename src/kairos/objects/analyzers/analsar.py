class UserObject(dict):
    def __init__(self):
        object = {
            "type": "analyzer",
            "id": "ANALSAR",
            "begin": self.begin,
            "end": self.end,
            "rules": [
                {"action": self.asarx, "regexp": r'([0-9]+)\/([0-9]+)\/([0-9]+).*$'},
                {"action": self.genstate(''), "regexp": r'^Average.*$'},
            ],
            "contextrules": [
                {"action": self.asarb0x, "regexp": r'^(..):(..):(..) +(.+?) +(.+?) +(.+?) +(.+?) +(.+?) +(.+?)[ \t]+(.+?)[ \t]+(.+?)$', "context": "sarb0", "scope": "SARB"},
                {"action": self.asarb1x, "regexp": r'^(..):(..):(..) (  |PM|AM) +(.+?) +(.+?) +(.+?) +(.+?) +(.+?)$', "context": "sarb1", "scope": "SARB"},
                {"action": self.asard0x, "regexp": r'^$|^(..):(..):(..) +(.+?) +(.+?) +(.+?) +(.+?) +(.+?) +(.+?) +(.+?)$|^ +(.+?) +(.+?) +(.+?) +(.+?) +(.+?) +(.+?) +(.+?)$', "context": "sard0", "scope": "SARD"},
                {"action": self.asard1x, "regexp": r'^(..):(..):(..) +(.+?) +([0-9]+.*?) +([0-9]+.*)$', "context": "sard1", "scope": "SARD"},
                {"action": self.asard2x, "regexp": r'(..):(..):(..) (  |PM|AM) +(.+?) +(.+?) +(.+?) +(.+?)$', "context": "sard2", "scope": "SARD"},
                {"action": self.asarn0x, "regexp": r'(..):(..):(..) (  |PM|AM) +(.+?) +(\d+\.\d+) +(.+?) +(.+?) +(.+?) +(.+?) +(.+?) +(.+?)$', "context": "sarn0", "scope": "SARN"},
                {"action": self.asarp0x, "regexp": r'^(..):(..):(..) (  |PM|AM) +(.+?) +(.+?)', "context": "sarp0", "scope": "SARP"},
                {"action": self.asarq0x, "regexp": r'^(..):(..):(..) +(.+?) +(.+?) +(.+?) +(.+?)$', "context": "sarq0", "scope": "SARQ"},
                {"action": self.asarq1x, "regexp": r'^(..):(..):(..) (  |PM|AM) +(.+?) +(.+?) +(.+?) +(.+?)$', "context": "sarq1", "scope": "SARQ"},
                {"action": self.asarm0x, "regexp": r'(..):(..):(..) +(.+?) +(.+?)$', "context": "sarm0", "scope": "SARQ"},
                {"action": self.asarm1x, "regexp": r'(..):(..):(..) (  |AM|PM) +(.+?) +(.+?) +(.+?) +(.+?) +(.+?) +(.+?) +(.+?) +(.+?) +(.+?)$', "context": "sarm1", "scope": "SARQ"},
                {"action": self.asaru0x, "regexp": r'(..):(..):(..) +(.+?) +(.+?) +(.+?) +(.+?)$', "context": "saru0", "scope": "SARU"},
                {"action": self.asaru1x, "regexp": r'(..):(..):(..) (  |PM|AM) +(all|[0-9]+) +(.+?) +(.+?) +(.+?) +(.+?)$', "context": "saru1", "scope": "SARU"},
                {"action": self.asaru2x, "regexp": r'(..):(..):(..) (  |PM|AM) +(all|[0-9]+) +(.+?) +(.+?) +(.+?) +(.+?) +(.+?)$', "context": "saru2", "scope": "SARU"},
                {"action": self.asaru3x, "regexp": r'(..):(..):(..) +(.+?) +(.+?) +(.+?) +(.+?) +([0-9]+\.[0-9][0-9])', "context": "saru3", "scope": "SARU"},
                {"action": self.asarv0x, "regexp": r'^(..):(..):(..).*? +([0-9]+)\/.*$', "context": "sarv0", "scope": "SARV"},
                {"action": self.asarw0x, "regexp": r'^(..):(..):(..) +(.+?) +(.+?)$', "context": "sarw0", "scope": "SARW"},
            ],
            "outcontextrules": [
                {"action": self.genstate("sarb0"), "regexp": r'^.*bread.*lread.*bwrit.*lwrit.*pread.*pwrit', "scope": "SARB"},
                {"action": self.genstate("sarb1"), "regexp": r'^.*tpself.*rtpself.*wtpself.*bread.*bwrtn', "scope": "SARB"},
                {"action": self.genstate("sard0"), "regexp": r'^.*device.*busy.*avque.*avwait.*avserv', "scope": "SARD"},
                {"action": self.genstate("sard1"), "regexp": r'DEV.*tpself.*blks/s', "scope": "SARD"},
                {"action": self.genstate("sard2"), "regexp": r'DEV.*tpself.*rd_sec/self.*wr_sec/s', "scope": "SARD"},
                {"action": self.genstate("sarn0"), "regexp": r'IFACE.*rxpck/self.*txpck/self.*rxbyt/self.*txbyt/self.*rxcmp/self.*txcmp/self.*rxmcst/s', "scope": "SARN"},
                {"action": self.genstate("sarp0"), "regexp": r'pgpgin/self.*pgpgout/s', "scope": "SARP"},
                {"action": self.genstate("sarq0"), "regexp": r'^.*runq-sz.*swpq-sz', "scope": "SARQ"},
                {"action": self.genstate("sarq1"), "regexp": r'runq-sz.*plist-sz.*ldavg-1.*ldavg-5', "scope": "SARQ"},
                {"action": self.genstate("sarm0"), "regexp": r'^.*freemem freesw[a]*p', "scope": "SARR"},
                {"action": self.genstate("sarm1"), "regexp": r'kbmemfree.*kbmemused.*%memused.*kbbufferself.*kbcached.*kbswpfree.*kbswpused.*%swpused', "scope": "SARR"},
                {"action": self.genstate("saru0"), "regexp": r'^.*usr.*syself.*wio.*idle', "scope": "SARU"},
                {"action": self.genstate("saru1"), "regexp": r'CPU.*%user.*%nice.*%system.*%idle', "scope": "SARU"},
                {"action": self.genstate("saru2"), "regexp": r'CPU.*%user.*%nice.*%syself.*%iowait.*%idle', "scope": "SARU"},
                {"action": self.genstate("saru2"), "regexp": r'CPU.*%usr.*%nice.*%syself.*%iowait.*%steal', "scope": "SARU"},
                {"action": self.genstate("saru3"), "regexp": r'^.*usr.*syself.*wio.*idle.*physc', "scope": "SARU"},
                {"action": self.genstate("sarv0"), "regexp": r'^.*proc-sz..*inod-sz.*file-sz', "scope": "SARV"},
                {"action": self.genstate("sarw0"), "regexp": r'pswpin/self.*pswpout/s', "scope": "SARW"},
                {"action": self.asarlcpu, "regexp": r'System configuration: lcpu=([0-9]+)'},
                {"action": self.asarent, "regexp": r'System configuration: lcpu=[0-9]+ ent=([0-9]+\.[0-9][0-9])'},
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
        a.tohour = lambda x,y: '00' if y=='AM'and int(x)>11 else str(int(x)+12) if y=='PM'and int(x)<12 else x

    def end(self, a):
        pass

    def genstate(self, c):
        def f(a, l ,g, m):
            a.setContext(c)
        return f

    def asarx(self, a, l, g, m):
        if len(g(3)) == 2:
            a.date = '20'+g(3)+g(1)+g(2)
        elif len(g(3)) == 4:
            a.date = g(3)+g(1)+g(2)

    def asarb0x(self, a, l, g, m):
        desc = dict(timestamp='text',bread='real',lread='real',bwrite='real',lwrite='real',pread='real',pwrite='real')
        a.emit('SARB', desc, dict(timestamp=a.date+g(1)+g(2)+g(3)+'000',bread=a.tof(g(4)),lread=a.tof(g(5)),bwrite=a.tof(g(7)),lwrite=a.tof(g(8)),pread=a.tof(g(10)),pwrite=a.tof(g(11))))

    def asarb1x(self, a, l, g, m):
        desc = dict(timestamp='text',bread='real',lread='real',bwrite='real',lwrite='real',pread='real',pwrite='real')
        a.emit('SARB', desc, dict(timestamp=a.date+a.tohour(g(1),g(4))+g(2)+g(3)+'000',bread=a.tof(g(8)),lread=0.0,bwrite=a.tof(g(9)),lwrite=0.0,pread=a.tof(g(6)),pwrite=a.tof(g(7))))

    def asard0x(self, a, l, g, m):
        desc = dict(timestamp='text',device='text',busy='real',avque='real',rws='real',kbs='real',avwait='real',avserv='real')
        if g(1):
            a.time=g(1)+g(2)+g(3)
            a.emit('SARD', desc, dict(timestamp=a.date+a.time+'000',device=g(4),busy=a.tof(g(5)),avque=a.tof(g(6)),rws=a.tof(g(7)),kbs=a.tof(g(8)),avwait=a.tof(g(9)),avserv=a.tof(g(10))))
        if g(11):
            a.emit('SARD', desc, dict(timestamp=a.date+a.time+'000',device=g(11),busy=a.tof(g(12)),avque=a.tof(g(13)),rws=a.tof(g(14)),kbs=a.tof(g(15)),avwait=a.tof(g(16)),avserv=a.tof(g(17))))

    def asard1x(self, a, l, g, m):
        desc = dict(timestamp='text',device='text',busy='real',avque='real',rws='real',kbs='real',avwait='real',avserv='real')
        a.emit('SARD', desc, dict(timestamp=a.date+g(1)+g(2)+g(3)+'000',device=g(4),busy=0.0,avque=0.0,rws=a.tof(g(5)),kbs=0.0,avwait=0.0,avserv=0.0))

    def asard2x(self, a, l, g, m):
        desc = dict(timestamp='text',device='text',busy='real',avque='real',rws='real',kbs='real',avwait='real',avserv='real')
        a.emit('SARD', desc, dict(timestamp=a.date+a.tohour(g(1),g(4))+g(2)+g(3)+'000',device=g(5),busy=0.0,avque=0.0,rws=a.tof(g(6))+a.tof(g(7)),kbs=0.0,avwait=0.0,avserv=0.0))

    def asarn0x(self, a, l, g, m):
        desc = dict(timestamp='text',iface='text',rxbyt='real',txbyt='real')
        a.emit('SARN', desc, dict(timestamp=a.date+a.tohour(g(1),g(4))+g(2)+g(3)+'000',iface=g(5),rxbyt=a.tof(g(8)),txbyt=a.tof(g(9))))

    def asarp0x(self, a, l, g, m):
        desc = dict(timestamp='text',pgpgin='real',pgpgout='real')
        a.emit('SARP', desc, dict(timestamp=a.date+a.tohour(g(1),g(4))+g(2)+g(3)+'000',pgpgin=a.tof(g(5)),pgpgout=a.tof(g(6))))

    def asarq0x(self, a, l, g, m):
        desc = dict(timestamp='text',runqsz='real',swpqsz='real')
        a.emit('SARQ', desc, dict(timestamp=a.date+g(1)+g(2)+g(3)+'000',runqsz=a.tof(g(4)),swpqsz=a.tof(g(6))))

    def asarq1x(self, a, l, g, m):
        desc = dict(timestamp='text',runqsz='real',swpqsz='real')
        a.emit('SARQ', desc, dict(timestamp=a.date+a.tohour(g(1),g(4))+g(2)+g(3)+'000',runqsz=a.tof(g(5)),swpqsz=0.0))

    def asarm0x(self, a, l, g, m):
        desc = dict(timestamp='text',kbmemfree='real',kbmemused='real',kbmemshrd='real',kbbuffers='real',kbcached='real',kbswpfree='real',kbswpused='real')
        a.emit('SARM', desc, dict(timestamp=a.date+g(1)+g(2)+g(3)+'000',kbmemfree=a.tof(g(4)),kbmemused=0.0,kbmemshrd=0.0,kbbuffers=0.0,kbcached=0.0,kbswpfree=a.tof(g(5)),kbswpused=0.0))

    def asarm1x(self, a, l, g, m):
        desc = dict(timestamp='text',kbmemfree='real',kbmemused='real',kbmemshrd='real',kbbuffers='real',kbcached='real',kbswpfree='real',kbswpused='real')
        a.emit('SARM', desc, dict(timestamp=a.date+a.tohour(g(1),g(4))+g(2)+g(3)+'000',kbmemfree=a.tof(g(5)),kbmemused=a.tof(g(6)),kbmemshrd=0.0,kbbuffers=a.tof(g(8)),kbcached=a.tof(g(9)),kbswpfree=a.tof(g(10)),kbswpused=a.tof(g(11))))

    def asaru0x(self, a, l, g, m):
        desc = dict(timestamp='text',cpuid='text',usr='real',sys='real',wio='real')
        a.emit('SARU', desc, dict(timestamp=a.date+g(1)+g(2)+g(3)+'000',cpuid='all',usr=a.tof(g(4)),sys=a.tof(g(5)),wio=a.tof(g(6))))

    def asaru1x(self, a, l, g, m):
        desc = dict(timestamp='text',cpuid='text',usr='real',sys='real',wio='real')
        a.emit('SARU', desc, dict(timestamp=a.date+a.tohour(g(1),g(4))+g(2)+g(3)+'000',cpuid=g(5),usr=a.tof(g(6)),sys=a.tof(g(8)),wio=0.0))

    def asaru2x(self, a, l, g, m):
        desc = dict(timestamp='text',cpuid='text',usr='real',sys='real',wio='real')
        a.emit('SARU', desc, dict(timestamp=a.date+a.tohour(g(1),g(4))+g(2)+g(3)+'000',cpuid=g(5),usr=a.tof(g(6)),sys=a.tof(g(8)),wio=a.tof(g(9))))

    def asaru3x(self, a, l, g, m):
        desc = dict(timestamp='text',cpuid='text',usr='real',sys='real',wio='real')
        corr=a.tof(g(8))/a.ent
        usr=a.tof(g(4))*corr
        sys=a.tof(g(5))*corr
        wio=a.tof(g(6))*corr
        a.emit('SARU', desc, dict(timestamp=a.date+g(1)+g(2)+g(3)+'000',cpuid='all',usr=usr,sys=sys,wio=wio))

    def asarv0x(self, a, l, g, m):
        desc = dict(timestamp='text',procsz='real')
        a.emit('SARV', desc, dict(timestamp=a.date+g(1)+g(2)+g(3)+'000',procsz=a.tof(g(4))))

    def asarw0x(self, a, l, g, m):
        desc = dict(timestamp='text',pswpin='real',pswpout='real')
        a.emit('SARW', desc, dict(timestamp=a.date+g(1)+g(2)+g(3)+'000',pswpin=a.tof(g(4)),pswpout=a.tof(g(5))))

    def asarlcpu(self, a, l, g, m):
        a.ent = a.tof(g(1)) / 2

    def asarent(self, a, l, g, m):
        a.ent = a.tof(g(1))
