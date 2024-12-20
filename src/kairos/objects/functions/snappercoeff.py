class UserObject(dict):
    def __init__(self):
        object = {
            "type": "function",
            "id": "snappercoeff",
            "name": "snappercoeff",
            "function": """
                CREATE OR REPLACE FUNCTION snappercoeff() RETURNS real AS $$
                    try: method = plpy.execute("select aggregatormethod from public.nodes where id = (select cast ( substr(current_schema(), 7) as integer))", 1)[0]['aggregatormethod']
                    except: method = '$none'
                    r = 1.0
                    if method == '$minute': r = 1.0
                    if method == '$5minutes': r = 5.0
                    if method == '$10minutes': r = 10.0
                    if method == '$15minutes': r = 15.0
                    if method == '$20minutes': r = 20.0
                    if method == '$30minutes': r = 30.0
                    if method == '$hour': r = 60.0
                    if method == '$2hours': r = 120.0
                    if method == '$3hours': r = 180.0
                    if method == '$4hours': r = 240.0
                    if method == '$6hours': r = 360.0
                    if method == '$8hours': r = 480.0
                    if method == '$12hours': r = 720.0
                    if method == '$day': r = 1440.0
                    return r
                $$ language plpython3u;
            """
        }
        super(UserObject, self).__init__(**object)
