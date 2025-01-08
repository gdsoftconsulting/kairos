class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "PGSYSDISK",
            "action": "dispchart",
            "chart": "PGSYSCHOOSEDISK",
            "query": "PGDISKCHOICE",
        }
        super(UserObject, self).__init__(**object)
