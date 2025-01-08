class UserObject(dict):
    def __init__(self):
        object = {
            "type": "function",
            "id": "bocoeff",
            "name": "bocoeff",
            "function": """
                CREATE OR REPLACE FUNCTION bocoeff() RETURNS real AS $$
                    try: method = plpy.execute("select aggregatormethod from public.nodes where id = (select cast ( substr(current_schema(), 7) as integer))", 1)[0]['aggregatormethod']
                    except: method = '$none'
                    r = 60.0
                    if method == '$minute': r = 60.0
                    if method == '$5minutes': r = 300.0
                    if method == '$10minutes': r = 600.0
                    if method == '$15minutes': r = 900.0
                    if method == '$20minutes': r = 1200.0
                    if method == '$30minutes': r = 1800.0
                    if method == '$hour': r = 3600.0
                    if method == '$2hours': r = 7200.0
                    if method == '$3hours': r = 10800.0
                    if method == '$4hours': r = 14400.0
                    if method == '$6hours': r = 21600.0
                    if method == '$8hours': r = 28800.0
                    if method == '$12hours': r = 43200.0
                    if method == '$day': r = 86400.0
                    return r
                $$ language plpython3u;
            """
        }
        super(UserObject, self).__init__(**object)
