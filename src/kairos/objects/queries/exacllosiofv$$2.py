null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "EXACLLOSIOFV$$2",
            "collections": [
                "EXATOPCLLOSIO"
            ],
            "userfunctions": [],
            "request": "select timestamp, label as label, avg(value) as value from (select timestamp, 'Flash disk maximum capacity for cell 1.5T'::text as label, 1372.0::real as value from EXATOPCLLOSIO union all select timestamp, 'Flash disk maximum capacity for cell 2.9T'::text as label, 1372.0::real as value from EXATOPCLLOSIO union all select timestamp, 'Flash disk maximum capacity for cell 186G'::text as label, 5488.0::real as value from EXATOPCLLOSIO) as foo group by timestamp, label order by timestamp",
            "nocache": true,
            "filterable": true
        }
        super(UserObject, self).__init__(**object)
