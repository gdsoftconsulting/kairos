null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "PGDATABASECHOICE",
            "collections": ["vkpg_stat_activity"],
            "request": "select distinct datname as label from vkpg_stat_activity order by label"
        }
        super(UserObject, self).__init__(**object)
