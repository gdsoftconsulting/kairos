class UserObject(dict):
    def __init__(self):
        object = {
            "type": "aggregator",
            "id": "$minute_v$",
            "name": "average_per_minute",
            "function": """
                CREATE OR REPLACE FUNCTION average_per_minute(x text) RETURNS text AS $$
	                return x[0:12] + "00000"
                $$ language plpython3u;
            """
        }
        super(UserObject, self).__init__(**object)
