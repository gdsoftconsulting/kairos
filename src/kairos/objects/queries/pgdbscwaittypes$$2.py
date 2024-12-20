null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "PGDBSCWAITTYPES$$2",
            "collections": [
                "vkpg_stat_activity"
            ],
            "userfunctions": [
                "pgdbscoeff"
            ],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, 'All backends'::text as label, 1.0 / pgdbscoeff(cast(snap_frequency as integer)) as value from vkpg_stat_activity where datname = '%(PGDBSCWAITTYPES)s') as foo group by timestamp, label order by timestamp",
            "nocache": true,
            "filterable": true
        }
        super(UserObject, self).__init__(**object)
