class UserObject(dict):
    def __init__(self):
        object = {
            "type": "aggregator",
            "id": "$4hours",
            "name": "average_per_4hours",
            "function": """
                CREATE OR REPLACE FUNCTION average_per_4hours(x text) RETURNS text AS $$
	                h = ["00", "04", "08", "12", "16", "20"][int(int(x[8:10]) / 4)]
	                return x[0:8] + h + "0000000"
                $$ language plpython3u;
            """
        }
        super(UserObject, self).__init__(**object)

