class UserObject(dict):
    def __init__(self):
        object = {
            "type": "aggregator",
            "id": "$15minutes",
            "name": "average_per_15minutes",
            "function": """
                CREATE OR REPLACE FUNCTION average_per_15minutes(x text) RETURNS text AS $$
                    m = ["00", "15", "30", "45"][int(int(x[10:12]) / 15)]
                    return x[0:10] + m + "00000"
                $$ language plpython3u;
            """
        }
        super(UserObject, self).__init__(**object)
