class UserObject(dict):
    def __init__(self):
        object = {
            "type": "aggregator",
            "id": "$12hours",
            "name": "average_per_12hours",
            "function": """
                CREATE OR REPLACE FUNCTION average_per_12hours(x text) RETURNS text AS $$
	                h = ["00", "12"][int(int(x[8:10]) / 12)]
	                return x[0:8] + h + "0000000"
                $$ language plpython3u;
            """
        }
        super(UserObject, self).__init__(**object)
