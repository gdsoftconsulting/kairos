class UserObject(dict):
    def __init__(self):
        object = {
            "type": "aggregator",
            "id": "$day",
            "name": "average_per_day",
            "function": """
                CREATE OR REPLACE FUNCTION average_per_day(x text) RETURNS text AS $$
	                return x[0:8] + "000000000"
                $$ language plpython3u;
            """
        }
        super(UserObject, self).__init__(**object)
