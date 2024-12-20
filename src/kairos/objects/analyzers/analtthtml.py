import hashlib
class UserObject(dict):
    def __init__(self):
        object = {
            "type": "analyzer",
            "id": "ANALTTHTML",
            "content": "xml",
            "begin": self.begin,
            "end": self.end,
            "rules": [
                {"action": self.ah2, "regexp": r'', "tag": 'h2'},
                {"action": self.atable, "regexp": r'', "tag": 'table'},
                {"action": self.atr, "regexp": r'', "tag": 'tr'},
                {"action": self.athd, "regexp": r'', "tag": '(th|td)'}
            ],
            "contextrules": [
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsum"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thmuc", "scope": "TTABSMETRICS"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thlp", "scope": "TTMETRICS"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thss", "scope": "TTSTATS"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsqlp", "scope": "TTSQLTOPP"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsqlx", "scope": "TTSQLTOPX"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thsqlt"},
                {"action": self.athget, "regexp": r'.', "tag": 'th', "context": "thprm", "scope": "TTPARAM"},
                {"action": self.atdget, "regexp": r'.', "tag": 'td', "context": "tdsum"},
                {"action": self.atdget, "regexp": r'.', "tag": 'td', "context": "tdmuc", "scope": "TTABSMETRICS"},
                {"action": self.atdget, "regexp": r'.', "tag": 'td', "context": "tdlp", "scope": "TTMETRICS"},
                {"action": self.atdget, "regexp": r'.', "tag": 'td', "context": "tdss", "scope": "TTSTATS"},
                {"action": self.atdget, "regexp": r'.', "tag": 'td', "context": "tdsqlp", "scope": "TTSQLTOPP"},
                {"action": self.atdget, "regexp": r'.', "tag": 'td', "context": "tdsqlx", "scope": "TTSQLTOPX"},
                {"action": self.atdget, "regexp": r'.', "tag": 'td', "context": "tdsqlt"},
                {"action": self.atdget, "regexp": r'.', "tag": 'td', "context": "tdprm", "scope": "TTPARAM"},
            ],
            "outcontextrules": [
                {"action": self.genstate('thsum'), "regexp": r'Summary', "tag": 'h2'},
                {"action": self.genstate('thss'), "regexp": r'Statement Statistics', "tag": 'h2', "scope": "TTSTATS"},
                {"action": self.genstate('thss'), "regexp": r'Transaction Statistics', "tag": 'h2', "scope": "TTSTATS"},
                {"action": self.genstate('thss'), "regexp": r'Log Statistics', "tag": 'h2', "scope": "TTSTATS"},
                {"action": self.genstate('thss'), "regexp": r'Checkpoint Statistics', "tag": 'h2', "scope": "TTSTATS"},
                {"action": self.genstate('thss'), "regexp": r'DB Activity Statistics', "tag": 'h2', "scope": "TTSTATS"},
                {"action": self.genstate('thss'), "regexp": r'Lock Statistics', "tag": 'h2', "scope": "TTSTATS"},
                {"action": self.genstate('thprm'), "regexp": r'Configuration Parameters', "tag": 'h2', "scope": "TTPARAM"},
                {"action": self.genstate('thsqlx'), "regexp": r'Executions% TotalCmd IDCmd Text', "tag": 'table', "scope": "TTSQLTOPX"},
                {"action": self.genstate('thsqlp'), "regexp": r'Preparations% TotalCmd IDCmd Text', "tag": 'table', "scope": "TTSQLTOPP"},
                {"action": self.genstate('thsqlt'), "regexp": r'SQL IDSQL Text', "tag": 'table', "scope": "TTSQLTEXT"},
                {"action": self.genstate('thsqlt'), "regexp": r'SQL IDSQL Text', "tag": 'table', "scope": "TTSQLTOPX"},
                {"action": self.genstate('thsqlt'), "regexp": r'SQL IDSQL Text', "tag": 'table', "scope": "TTSQLTOPP"},
                {"action": self.genstate('thmuc'), "regexp": r'MetricsBegin ValueEnd Value', "tag": 'table', "scope": "TTABSMETRICS"},
                {"action": self.genstate('thlp'), "regexp": r'MetricsPer SecondPer Transaction', "tag": 'table', "scope": "TTMETRICS"},
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
        convertid=dict()
        tof=lambda x: float(x.replace(',','').replace(u'\xa0','0')) if x!=u'' else 0.0
        for x in sorted(a.collected.keys(),reverse=True):
            if x =='zz9':
                dttmisc = dict(timestamp='text', avgelapsed='real', elapsed='int')
                for y in a.collected[x]:
                    when = y['Info']
                    what = y['Snap Time']
                    if when == 'End Snap:':
                        year = str(what[0:4])
                        month = str(what[5:7])
                        day = str(what[8:10])
                        hour = str(what[11:13])
                        min = str(what[14:16])
                        sec = str(what[17:19])
                        a.date = year + month + day + hour + min + sec + "000"
                    if when == 'Elapsed Time:':
                        a.dur = int(tof(what[:-4]))
                        if 'TTMISC' in a.scope: a.emit('TTMISC', dttmisc, dict(timestamp=a.date, avgelapsed=float(a.dur), elapsed=int(a.dur)))
            if 'MetricsBegin ValueEnd Value' in x:
                d = dict(timestamp='text', metric='text', averagedvalue='real', summedvalue='int')
                for y in a.collected[x]:
                    metric = y['Metrics']
                    averagedvalue = tof(y['End Value'])
                    summedvalue = int(y['End Value'])
                    a.emit('TTABSMETRICS', d, dict(timestamp=a.date, metric=metric, averagedvalue=averagedvalue, summedvalue=summedvalue))
            if 'MetricsPer SecondPer Transaction' in x:
                d = dict(timestamp='text', metric='text', value='real')
                for y in a.collected[x]:
                    metric = y['Metrics']
                    value = tof(y['Per Second'])
                    a.emit('TTMETRICS', d, dict(timestamp=a.date, metric=metric, value=value))
            if 'Statement Statistics' in x or 'Transaction Statistics' in x or 'Log Statistics' in x or 'Checkpoint Statistics' in x or 'DB Activity Statistics' in x or 'Lock Statistics' in x:
                d = dict(timestamp='text', statistic='text', value='real')
                for y in a.collected[x]:
                    statistic = y['Statistics']
                    value = tof(y['Rate (Per Second)'])
                    a.emit('TTSTATS', d, dict(timestamp=a.date, statistic=statistic, value=value))
            if 'Preparations% TotalCmd IDCmd Text' in x:
                d = dict(timestamp='text', sqlid='text', hashid='text', prepares='real', percent='real')
                for y in a.collected[x]:
                    sqlid = y['Cmd ID']
                    hashid = convertid[sqlid]
                    prepares = tof(y['Preparations']) / a.dur
                    percent = tof(y['% Total'])
                    a.emit('TTSQLTOPP', d, dict(timestamp=a.date, sqlid=sqlid, hashid=hashid, prepares=prepares, percent=percent))
            if 'Executions% TotalCmd IDCmd Text' in x:
                d = dict(timestamp='text', sqlid='text', hashid='text', execs='real', percent='real')
                for y in a.collected[x]:
                    sqlid = y['Cmd ID']
                    hashid = convertid[sqlid]
                    execs = tof(y['Executions']) / a.dur
                    percent = tof(y['% Total'])
                    a.emit('TTSQLTOPX', d, dict(timestamp=a.date, sqlid=sqlid, hashid=hashid, execs=execs, percent=percent))
            if 'SQL IDSQL Text' in x:
                d = dict(sqlid='text', hashid='text', request='text')
                for y in a.collected[x]:
                    sqlid = y['SQL ID']
                    request = y['SQL Text']
                    convertid[sqlid] = hashlib.md5(request.encode()).hexdigest()
                    hashid = convertid[sqlid]
                    if 'TTSQLTEXT' in a.scope: a.emit('TTSQLTEXT', d, dict(sqlid=sqlid, hashid=hashid, request=request))
            if 'Configuration Parameters' in x:
                d = dict(parameter='text', begvalue='text', endvalue='text')
                for y in a.collected[x]:
                    parameter = y['Paramter']
                    begvalue = y['Begin Value']
                    endvalue = y['End Value']
                    a.emit('TTPARAM', d, dict(parameter=parameter, begvalue=begvalue, endvalue=endvalue))

    def ah2(self, a, l, g, m):
        context = ''
        a.setContext(context)
        if len(a.row): a.tab.append(a.row)
        a.row = {}
        a.cpt = -1
        a.collector = {}

    def atable(self, a, l, g, m):
        context = ''
        if a.reinit: a.setContext(context)
        if len(a.scope) < 3:
            if a.scope.issubset({'TTMISC'}) and 'zz9' in a.collected: a.setContext('BREAK')
            if a.scope.issubset({'TTPARAM'}) and 'Configuration Parameters' in a.collected and len(a.collected['Configuration Parameters']): a.setContext('BREAK')
            if a.scope.issubset({'TTABSMETRICS'}) and 'MetricsBegin ValueEnd Value' in a.collected and len(a.collected['MetricsBegin ValueEnd Value']): a.setContext('BREAK')
            if a.scope.issubset({'TTMETRICS'}) and 'MetricsPer SecondPer Transaction' in a.collected and len(a.collected['MetricsPer SecondPer Transaction']): a.setContext('BREAK')
            if a.scope.issubset({'TTSQLTOPP'}) and 'Preparations% TotalCmd IDCmd Text' in a.collected and len(a.collected['Preparations% TotalCmd IDCmd Text']): a.setContext('BREAK')
            if a.scope.issubset({'TTSQLTOPX'}) and 'Executions% TotalCmd IDCmd Text' in a.collected and len(a.collected['Executions% TotalCmd IDCmd Text']): a.setContext('BREAK')
            if a.scope.issubset({'TTSQLTEXT'}) and 'SQL IDSQL Text' in a.collected and len(a.collected['SQL IDSQL Text']): a.setContext('BREAK')
        if len(a.row): a.tab.append(a.row)
        a.row = {}
        a.collector = {}

    def athget(self, a, l, g, m):
        if 0 not in a.collector: a.collector[0] = ''
        a.collector[a.cpt]=a.lxmltext(l)

    def atdget(self, a, l, g, m):
        if a.cpt in a.collector: a.row[a.collector[a.cpt]]=a.lxmltext(l)

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
            if k == 'Summary': k = 'zz9'
            a.collected[k] = a.tab
        return f
