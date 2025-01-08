#   GENERIC reports have the following format:
#
#   REPORT TYPE: GENERIC [SEP1="xxx",SEP2="yyy",ENCODING="eee"]
#                3 optional parameters separated by ","
#                SEP1 separator of fields, default value ","
#                SEP2 separator for key/value, default value "="
#                ENCODING code used to encode string, default value "ascii" ("hex" can be used to encode complex strings like SQL)
#   REPORT TYPE: COMPACT [ENCODING="eee",INITIAL="YYYYMMDDHHMISS"]
#                2 optional parameters separated by ","
#                ENCODING code used to encode string, default value "ascii" ("hex" can be used to encode complex strings like SQL)
#                INITIAL specifies the first date from which timestamp are computed (no default value)
#   TYPE table column name type
#                allows to define a specific type for a column of a table
#   20070227183245 EMP name=SCOTT,job=CLERK,salary=1500
#   20070227183246 DEPT location=NEW YORK,name=ACCOUNTING
#                The first field is a timestamp in the following format: YYYYMMDDHHMISS
#                The second field is the name of the table
#                the third field is splitted using SEP1 and SEP2
#   E/EMP , name=text,job=text,salary=real
#   D/DEPT ;; location=text,name=text
#   E/20070227183245,SCOTT,CLERK,1500
#   D/20070227183246;;NEW YORK;;ACCOUNTING

import datetime, logging

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "analyzer",
            "id": "ANALGEN",
            "begin": self.begin,
            "end": self.end,
            "rules": [],
            "contextrules": [
                {"action": self.ageneric, "regexp": r'^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2}) (\w+) (.+)$', "context": "generic"},
                {"action": self.acompact, "regexp": r'^(\w{1})\/(\d+.+)$', "context": "compact"}
            ],
            "outcontextrules": [
                {"action": self.asep, "regexp": r'^REPORT TYPE: GENERIC SEP1="(.+?)",SEP2="(.+?)".*$'},
                {"action": self.aencoding, "regexp": r'^REPORT TYPE: COMPACT ENCODING="(.+?)",INITIAL="(.+?)".*$'},
                {"action": self.adescfield, "regexp": r'^TYPE (.+) (.+) (.+) *$'},
                {"action": self.astartdata, "regexp": r'^(\d{14}) (\w+) (.+)$'},
                {"action": self.adesctable, "regexp": r'^(\w{1})\/(\w+) (.+) (.+) *$'},
                {"action": self.astartdata, "regexp": r'^(\w{1})\/(\d+.+)$'}
            ]
        }
        super(UserObject, self).__init__(**object)

    def begin(self, a):
        a.sep1 = ","
        a.sep2 = "="
        a.initial = "00000000000000"
        a.encoding = "ascii"
        a.compact = False
        a.alias = {}
        a.desctable = {}
        a.transform = {}
        a.separator = {}
        a.columns = {}
        a.ftype = {}

    def end(self, a):
        pass

    def asep(self, a, l ,g, m):
        a.sep1 = g(1)
        a.sep2 = g(2)

    def aencoding(self, a, l ,g, m):
        a.compact = True
        a.encoding = g(1)
        a.initial = g(2)

    def adescfield(self, a, l ,g, m):
        tname = g(1)
        noop = lambda x: x
        def trint(x):
            try: v = int(x)
            except: v = x
            return v
        def trnumber(x):
            try: v = float(x)
            except: v = x
            return v
        if tname not in a.transform:
            a.transform[tname] = dict(timestamp=noop, kairos_count=trint)
            a.desctable[tname] = dict(timestamp='text', kairos_count='bigint')
        f = trint if g(3) == 'int' else noop
        f = trnumber if g(3) == 'real' else f
        a.transform[tname][g(2)] = f
        a.desctable[tname][g(2)] = g(3) if g(3) != 'int' else 'bigint'

    def adesctable(self, a, l ,g, m):
        alias = g(1)
        tname = g(2)
        a.alias[alias] = tname
        a.desctable = dict(timestamp='text')
        a.separator[alias] = g(3)
        a.columns[alias] = [['timestamp','text']]
        for x in g(4).split(','):
            [b,v] = x.split('=')
            a.columns[alias].append([b,v])
            a.desctable[b] = v
        a.columns[alias].append(['kairos_count','bigint'])
        a.desctable['kairos_count'] = 'bigint'

    def astartdata(self, a, l ,g, m):
        if a.compact: a.setContext('compact')
        else:
            tname = g(2)
            noop = lambda x: x
            def trint(x):
                try: v = int(x)
                except: v = x
                return v
            def trnumber(x):
                try: v = float(x)
                except: v = x
                return v
            if tname not in a.transform:
                a.transform[tname] = dict(timestamp=noop, kairos_count=trint)
                a.desctable[tname] = dict(timestamp='text', kairos_count='bigint')
            d = dict()
            for p in g(3).split(a.sep1):
                [b,v] = p.split(a.sep2)
                d[b] = v
            for k in d:
                if k not in a.transform[tname]:
                    a.transform[tname][k] = trnumber if d[k].isdigit() else noop
                    a.desctable[tname][k] = 'real' if d[k].isdigit() else 'text'
            a.setContext('generic')

    def ageneric(self, a, l ,g, m):
        tname = g(7)
        try:
            d = dict(timestamp = g(1) + g(2) + g(3) + g(4) + g(5) + g(6) + "000", kairos_count = 1)
            for p in g(8).split(a.sep1):
                [k, v] = p.split(a.sep2)
                d[k] = a.transform[tname][k](v)
            for k in a.desctable[tname]:
                if k not in d: d[k] = ''
            a.emit(tname, a.desctable[tname], d)
        except: logging.error(f'Exception when parsing the line containing {l}')

    def acompact(self, a, l ,g, m):
        alias = g(1)
        tname = a.alias[alias]
        separator = a.separator[alias]
        d = dict()
        i = 0
        for x in g(2).split(separator):
            column = a.columns[alias][i][0]
            coltype = a.columns[alias][i][1]
            if column == 'timestamp':
                if a.initial=='00000000000000':
                    d['timestamp'] = x if int(x) else a.initial
                else:
                    start = datetime.datetime.strptime(a.initial, '%Y%m%d%H%M%S')
                    delta = int(x) * 1.0 / 24 / 3600
                    d['timestamp'] = datetime.datetime.strftime(start + delta, '%Y%m%d%H%M%S')
            else:
                if coltype == 'text':
                    x = x.decode(a.encoding)
                    #if type(x) != type(u''): x = unicode(x,'utf-8','replace')
                if coltype == 'int':
                    try: x = int(x)
                    except: pass
                if coltype == 'real':
                    try: x = float(x)
                    except: pass
                d[column] = x
            i+=1
        d['kairos_count']=1
        a.emit(tname, a.desctable, d)
