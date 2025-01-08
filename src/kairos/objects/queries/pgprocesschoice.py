null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "PGPROCESSCHOICE",
            "collections": ["vpsutil_processes"],
            "request": "select distinct pname||' - '||pid||' - '||create_time as label from vpsutil_processes order by label"
        }
        super(UserObject, self).__init__(**object)
