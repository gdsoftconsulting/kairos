null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORASYS$$3",
            "collections": [
                "DBORAOSS",
                "DBORAMISC"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, statistic as label, value*1.0/100/avgelapsed as value from (select t.timestamp, statistic, value, avgelapsed from DBORAOSS as t, DBORAMISC as m where t.timestamp=m.timestamp and t.kairos_nodeid=m.kairos_nodeid) as foo where statistic in ('OS_CPU_WAIT_TIME') union all select timestamp, statistic as label, value as value from (select t.timestamp, statistic, value, avgelapsed from DBORAOSS as t, DBORAMISC as m where t.timestamp=m.timestamp and t.kairos_nodeid=m.kairos_nodeid) as foo where statistic in ('LOAD')) as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": false
        }
        super(UserObject, self).__init__(**object)
