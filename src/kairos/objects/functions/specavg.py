class UserObject(dict):
    def __init__(self):
        object = {
            "type": "function",
            "id": "specavg",
            "name": "specavg",
            "function": """
                CREATE OR REPLACE FUNCTION specavg(x real, y text, z text, t jsonb) RETURNS real AS $$
                    import json
                    d = json.loads(t)
                    return None if x == None else x / d[y+z]
                $$ language plpython3u;
            """
        }
        super(UserObject, self).__init__(**object)
