class UserObject(dict):
    def __init__(self):
        object = {
            "type": "aggregator",
            "id": "$month",
            "name": "average_per_month",
            "function": """
                CREATE OR REPLACE FUNCTION average_per_month(x text) RETURNS text AS $$
	                return x[0:6] + "00000000000"
                $$ language plpython3u;
            """
        }
        super(UserObject, self).__init__(**object)
