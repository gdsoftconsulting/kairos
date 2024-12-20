null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "PGDBSREFTIME",
            "collections": ["vkpg_stat_activity"],
            "request": "select distinct timestamp from vkpg_stat_activity"
        }
        super(UserObject, self).__init__(**object)
