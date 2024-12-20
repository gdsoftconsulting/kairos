class UserObject(dict):
    def __init__(s):
        object = {
            "type": "query",
            "id": "DBORAASHDBTIME$$1",
            "collections": [
                "ORAHAS"
            ],
            "userfunctions": [
                "ashcoeff"
            ],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, 'DB time'::text as label, kairos_count * 1.0 /ashcoeff as value from ORAHAS, (select ashcoeff() as ashcoeff) as foo where session_type = 'FOREGROUND') as foo group by timestamp, label order by timestamp",
            "nocache": false,
            "filterable": true
        }
        super(UserObject, s).__init__(**object)