import numpy
from datetime import datetime, timedelta
class UserObject(dict):
    def __init__(self):
        object = {
            "type": "analyzer",
            "id": "ANALBO",
            "begin": self.begin,
            "end": self.end,
            "rules": [],
            "contextrules": [
                {"action": self.ageneric, "regexp": r'^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2}) (\w+) (.+)$', "context": "generic"},
            ],
            "outcontextrules": [
                {"action": self.asep, "regexp": r'^REPORT TYPE: BO SEP1="(.+?)",SEP2="(.+?)".*$'},
                {"action": self.adescfield, "regexp": r'^TYPE (.+) (.+) (.+) *$'},
                {"action": self.astartdata, "regexp": r'^(\d{14}) (\w+) (.+)$'},
            ]
        }
        super(UserObject, self).__init__(**object)

    def begin(self, a):
        a.sep1 = ","
        a.sep2 = "="
        a.key = 0
        a.data = {}
        a.bins = {}
        a.initial = "00000000000000"
        a.encoding = "ascii"
        a.alias = {}
        a.desctable = {}
        a.transform = {}
        a.separator = {}
        a.columns = {}
        a.ftype = {}

    def end(self, a):
        a.desctable["BOBO2"]["executecount"] = 'bigint'
        for k in sorted(a.data):
            accumulator = 0.0
            for eid in sorted(a.data[k]):
                t0 = a.data[k][eid]['timestamp']
                pt0 = datetime.strptime(t0, '%Y%m%d%H%M%S')
                pt1 = pt0 + timedelta(accumulator)
                a.data[k][eid]['beginterval'] = pt1
                a.bins[pt1] = None
                accumulator += float(a.data[k][eid]['duration']) / (24 * 3600)
                pt2 = pt0 + timedelta(accumulator)
                a.data[k][eid]['endinterval'] = pt2
                a.bins[pt2] = None
        a.bins = sorted(a.bins)
        vmin = a.bins[0]
        vmax = a.bins[-1]
        binf = datetime(vmin.year, vmin.month, vmin.day, vmin.hour, vmin.minute)
        bsup = datetime(vmax.year, vmax.month, vmax.day, vmax.hour, vmax.minute) + timedelta(1.0 / 24 / 60)
        bins = range(int((bsup - binf).total_seconds() / 60))
        stack = []
        for k in sorted(a.data):
            for eid in sorted(a.data[k]):
                newdata = dict()
                x1 = a.data[k][eid]['beginterval']
                y1 = datetime(x1.year, x1.month, x1.day, x1.hour, x1.minute)
                b1 = (y1 - binf).total_seconds() / 60
                x2 = a.data[k][eid]['endinterval']
                y2 = datetime(x2.year, x2.month, x2.day, x2.hour, x2.minute)
                b2 = (y2 - binf).total_seconds() / 60
                delta = delta1 = delta2 = 0
                if x1 >= y2: delta = int((x2 - x1).total_seconds())
                if x1 < y2:
                    delta1 = int((y1 + timedelta(1.0 / 24 / 60) - x1).total_seconds())
                    delta2 = int((x2 - y2).total_seconds())
                x = numpy.histogram([b1, b2], bins=bins)
                y = [i for i in range(len(x[0])) if x[0][i]]
                for i in range(min(y), max(y)+1):
                    for j in a.data[k][eid]:
                        if j not in ['beginterval', 'endinterval', 'timestamp']: newdata[j] = a.data[k][eid][j]
                    newdata['timestamp'] = datetime.strftime(binf + timedelta(float(i) / 60 / 24), '%Y%m%d%H%M') + '00000'
                    if len(y) == 1:
                        newdata['executecount'] = delta
                    if len(y) == 2:
                        if i == y[0]:
                            newdata['executecount'] = delta1
                        if y[0] < i and i < y[1]:
                            newdata['executecount'] = 60
                        if i == y[1]:
                            newdata['executecount'] = delta2
                    stack.append(newdata)
        a.emit("BO", a.desctable["BOBO2"], stack)

    def asep(self, a, l ,g, m):
        a.sep1 = g(1)
        a.sep2 = g(2)

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

    def astartdata(self, a, l ,g, m):
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
        d = dict(timestamp = g(1) + g(2) + g(3) + g(4) + g(5) + g(6), kairos_count = 1)
        for p in g(8).split(a.sep1):
            [k, v] = p.split(a.sep2)
            d[k] = a.transform[tname][k](v)
        for k in a.desctable[tname]:
            if k not in d: d[k] = None
        a.key = str(d['timestamp']) + d['Report'] + d['user_name']
        if a.key not in a.data: a.data[a.key] = dict()
        a.data[a.key][d['event_id']] = d
