class UserObject(dict):
    def __init__(self):
        object = {
            "type": "aggregator",
            "id": "$2hours",
            "name": "average_per_2hours",
            "function": """
                CREATE OR REPLACE FUNCTION average_per_2hours(x text) RETURNS text AS $$
	                h = ["00", "02", "04", "06", "08", "10", "12", "14", "16", "18", "20", "22"][int(int(x[8:10]) / 2)]
	                return x[0:8] + h + "0000000"
                $$ language plpython3u;
            """
        }
        super(UserObject, self).__init__(**object)
