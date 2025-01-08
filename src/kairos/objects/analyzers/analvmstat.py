from datetime import datetime, timedelta
class UserObject(dict):
    def __init__(self):
        object = {
            "type": "analyzer",
            "id": "ANALVMSTAT",
            "begin": self.begin,
            "end": self.end,
            "rules": [],
            "contextrules": [
                {"action": self.vmstat, "regexp": r'^(\d+):(\d+):(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+)', "context": "vmstat", "scope": "VMSTAT"},
            ],
            "outcontextrules": [
                {"action": self.date, "regexp": r'^.*Starting Time:\s+(\d+)/(\d+)/(\d+)', "scope": "VMSTAT"},
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
        a.lasttime = "000000"
        a.tohour = lambda x,y: '00' if y=='AM'and int(x)>11 else str(int(x)+12) if y=='PM'and int(x)<12 else x

    def end(self, a):
        pass

    def date(self, a, l, g, m):
        a.date = g(3)+g(1)+g(2)
        a.desc = dict(timestamp='text',vms_r='real',vms_b='real',vms_swpd='real',vms_free='real',vms_buff='real',vms_cache='real',vms_si='real',vms_so='real',vms_bi='real',vms_bo='real',vms_in='real',vms_cs='real',vms_us='real',vms_sy='real',vms_id='real',vms_wa='real',vms_st='real')
        a.setContext('vmstat')

    def vmstat(self, a, l, g, m):
        a.time = g(1) + g(2) + g(3)
        if a.time < a.lasttime:
            a.date = datetime.strftime(datetime.strptime(a.date, '%Y%m%d') + timedelta(1), '%Y%m%d')
        a.lasttime = a.time
        a.emit('VMSTAT', a.desc, dict(timestamp=a.date+g(1)+g(2)+g(3)+'000',vms_r=a.tof(g(4)),vms_b=a.tof(g(5)),vms_swpd=a.tof(g(6)),vms_free=a.tof(g(7)),vms_buff=a.tof(g(8)),vms_cache=a.tof(g(9)),vms_si=a.tof(g(10)),vms_so=a.tof(g(11)),vms_bi=a.tof(g(12)),vms_bo=a.tof(g(13)),vms_in=a.tof(g(14)),vms_cs=a.tof(g(15)),vms_us=a.tof(g(16)),vms_sy=a.tof(g(17)),vms_id=a.tof(g(18)),vms_wa=a.tof(g(19)),vms_st=a.tof(g(20))))