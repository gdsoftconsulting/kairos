null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAASHSQLPHV$$1",
            "collections": [
                "ORAHAS"
            ],
            "userfunctions": [
                "ashcoeff"
            ],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, sql_plan_hash_value||' - '||sql_id as label, kairos_count * 1.0 /ashcoeff as value from ORAHAS, (select ashcoeff() as ashcoeff) as foo where sql_id = '%(DBORAASHSQLPHV)s') as foo group by timestamp, label order by timestamp",
            "nocache": true,
            "filterable": true
        }
        super(UserObject, self).__init__(**object)
