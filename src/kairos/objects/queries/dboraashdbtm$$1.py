null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAASHDBTM$$1",
            "collections": [
                "ORAHAS"
            ],
            "userfunctions": [
                "ashcoeff"
            ],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, 'IN_SQL_EXECUTION'::text as label, kairos_count * 1.0 /ashcoeff as value from ORAHAS, (select ashcoeff() as ashcoeff) as foo where session_type = 'FOREGROUND' and IN_SQL_EXECUTION = 'Y' union all select timestamp, 'IN_PARSE'::text as label, kairos_count * 1.0 /ashcoeff as value from ORAHAS, (select ashcoeff() as ashcoeff) as foo where session_type = 'FOREGROUND' and IN_PARSE = 'Y' union all select timestamp, 'IN_HARD_PARSE'::text as label, kairos_count * 1.0 /ashcoeff as value from ORAHAS, (select ashcoeff() as ashcoeff) as foo where session_type = 'FOREGROUND' and IN_HARD_PARSE = 'Y' union all select timestamp, 'IN_BIND'::text as label, kairos_count * 1.0 /ashcoeff as value from ORAHAS, (select ashcoeff() as ashcoeff) as foo where session_type = 'FOREGROUND' and IN_BIND = 'Y') as foo group by timestamp, label order by timestamp",
            "nocache": true,
            "filterable": true
        }
        super(UserObject, self).__init__(**object)
