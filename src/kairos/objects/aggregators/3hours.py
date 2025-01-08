class UserObject(dict):
    def __init__(self):
        object = {
            "type": "aggregator",
            "id": "$3hours",
            "name": "average_per_3hours",
            "function": """
                CREATE OR REPLACE FUNCTION average_per_3hours(x text) RETURNS text AS $$
	                h = ["00", "03", "06", "09", "12", "15", "18", "21"][int(int(x[8:10]) / 3)]
	                return x[0:8] + h + "0000000"
                $$ language plpython3u;
            """
        }
        super(UserObject, self).__init__(**object)
