class UserObject(dict):
    def __init__(self):
        object = {
            "type": "aggregator",
            "id": "$20minutes",
            "name": "average_per_20minutes",
            "function": """
                CREATE OR REPLACE FUNCTION average_per_20minutes(x text) RETURNS text AS $$
                    m = ["00", "20", "40"][int(int(x[10:12]) / 20)]
                    return x[0:10] + m + "00000"
                $$ language plpython3u;
            """
        }
        super(UserObject, self).__init__(**object)
