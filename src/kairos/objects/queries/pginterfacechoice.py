null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "PGINTERFACECHOICE",
            "collections": ["vpsutil_net_io_counters"],
            "request": "select distinct iface as label from vpsutil_net_io_counters order by label"
        }
        super(UserObject, self).__init__(**object)
