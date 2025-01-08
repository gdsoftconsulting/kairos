null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "PGSYSCHOOSEINTERFACE$$1",
            "collections": [
                "vpsutil_net_io_counters"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, avg(value) as value from (select timestamp, 'Average volume per received packet'::text as label, (case when packets_recv = 0 then 0.0 else bytes_recv / packets_recv end) as value from vpsutil_net_io_counters where iface = '%(PGSYSINTERFACE)s'::text union all select timestamp, 'Average volume per sent packet'::text as label, (case when packets_sent = 0 then 0.0 else bytes_sent / packets_sent end) as value from vpsutil_net_io_counters where iface = '%(PGSYSINTERFACE)s'::text) as foo group by timestamp, label order by timestamp",
            "nocache": true,
            "filterable": false
        }
        super(UserObject, self).__init__(**object)
