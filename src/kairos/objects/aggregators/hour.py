class UserObject(dict):
    def __init__(self):
        object = {
            "type": "aggregator",
            "id": "$hour",
            "name": "average_per_hour",
            "function": """
                CREATE OR REPLACE FUNCTION average_per_hour(x text) RETURNS text AS $$
	                return x[0:10] + "0000000"
                $$ language plpython3u;
            """
        }
        super(UserObject, self).__init__(**object)
