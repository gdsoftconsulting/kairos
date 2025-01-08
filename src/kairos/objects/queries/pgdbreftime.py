null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "PGDBREFTIME",
            "collections": ["vkpg_stat_database"],
            "request": "select distinct timestamp from vkpg_stat_database"
        }
        super(UserObject, self).__init__(**object)
