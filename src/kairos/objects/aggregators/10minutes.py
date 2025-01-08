class UserObject(dict):
    def __init__(self):
        object = {
            "type": "aggregator",
            "id": "$10minutes",
            "name": "average_per_10minutes",
            "function": """
                CREATE OR REPLACE FUNCTION average_per_10minutes(x text) RETURNS text AS $$
                    return x[0:11] + "000000"
                $$ language plpython3u;
            """
        }
        super(UserObject, self).__init__(**object)
