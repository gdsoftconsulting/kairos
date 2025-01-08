class UserObject(dict):
    def __init__(self):
        object = {
            "type": "aggregator",
            "id": "$5minutes",
            "name": "average_per_5minutes",
            "function": """
                CREATE OR REPLACE FUNCTION average_per_5minutes(x text) RETURNS text AS $$
                    m = ["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"][int(int(x[10:12]) / 5)]
                    return x[0:10] + m + "00000"
                $$ language plpython3u;
            """
        }
        super(UserObject, self).__init__(**object)
