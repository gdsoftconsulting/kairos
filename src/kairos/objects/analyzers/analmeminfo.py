from datetime import datetime, timedelta
class UserObject(dict):
    def __init__(self):
        object = {
            "type": "analyzer",
            "id": "ANALMEMINFO",
            "begin": self.begin,
            "end": self.end,
            "rules": [],
            "contextrules": [
                {"action": self.meminfo, "regexp": r'^(\w+): +(\d+) kB', "context": "meminfo", "scope": "MEMINFO"},
            ],
            "rules": [
                {"action": self.date, "regexp": r'^zzz \<(\d+)/(\d+)/(\d+) (\d+):(\d+):(\d+)\> Count', "scope": "MEMINFO"},
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

    def date(self, a, l, g, m):
        a.date = g(3)+g(1)+g(2)+g(4)+g(5)+g(6)+'000'
        a.desc = dict(timestamp='text',statistic='text',value='real')
        a.setContext('meminfo')

    def meminfo(self, a, l, g, m):
        a.emit('MEMINFO', a.desc, dict(timestamp=a.date,statistic=g(1),value=a.tof(g(2))))