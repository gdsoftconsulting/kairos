null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "PGSYSCHOOSEINTERFACE$$3",
            "collections": [
                "vpsutil_net_io_counters"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, avg(value) as value from (select timestamp, 'Average received packets per second'::text as label, packets_recv as value from vpsutil_net_io_counters where iface = '%(PGSYSINTERFACE)s'::text union all select timestamp, 'Average sent packets per second'::text as label, packets_sent as value from vpsutil_net_io_counters where iface = '%(PGSYSINTERFACE)s'::text) as foo group by timestamp, label order by timestamp",
            "nocache": true,
            "filterable": false
        }
        super(UserObject, self).__init__(**object)
