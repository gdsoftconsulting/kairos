null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAHPHVSX$$6",
            "collections": [
                "ORAHQS"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, sum(value) as value from (select timestamp, 'Rows processed'::text as label, value as value from (select timestamp, sum(rows_processed_delta::real) * 1.0 / (case when sum(executions_delta::real) = 0 then 1 else sum(executions_delta::real) end) as value from ORAHQS where plan_hash_value = '%(DBORAHPHVSX)s' group by timestamp) as foo) as foo group by timestamp, label order by timestamp",
            "nocache": true,
            "filterable": false
        }
        super(UserObject, self).__init__(**object)