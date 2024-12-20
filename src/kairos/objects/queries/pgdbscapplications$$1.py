null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "PGDBSCAPPLICATIONS$$1",
            "collections": [
                "vkpg_stat_activity"
            ],
            "userfunctions": [
                "pgdbscoeff"
            ],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, application_name as label, 1.0 / pgdbscoeff(cast(snap_frequency as integer)) as value from vkpg_stat_activity where datname = '%(PGDBSCAPPLICATIONS)s' and state = 'active' ) as foo group by timestamp, label order by timestamp",
            "nocache": true,
            "filterable": true
        }
        super(UserObject, self).__init__(**object)
