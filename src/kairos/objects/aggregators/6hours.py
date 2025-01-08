class UserObject(dict):
    def __init__(self):
        object = {
            "type": "aggregator",
            "id": "$6hours",
            "name": "average_per_6hours",
            "function": """
                CREATE OR REPLACE FUNCTION average_per_6hours(x text) RETURNS text AS $$
	                h = ["00", "06", "12", "18"][int(int(x[8:10]) / 6)]
	                return x[0:8] + h + "0000000"
                $$ language plpython3u;
            """
        }
        super(UserObject, self).__init__(**object)

