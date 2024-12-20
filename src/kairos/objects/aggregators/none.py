class UserObject(dict):
    def __init__(self):
        object = {
            "type": "aggregator",
            "id": "$none",
            "name": "no_average",
            "function": """
                CREATE OR REPLACE FUNCTION no_average(x text) RETURNS text AS $$
	                return x
                $$ language plpython3u;
            """
        }
        super(UserObject, self).__init__(**object)
