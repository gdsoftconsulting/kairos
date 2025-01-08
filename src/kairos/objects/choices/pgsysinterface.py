class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "PGSYSINTERFACE",
            "action": "dispchart",
            "chart": "PGSYSCHOOSEINTERFACE",
            "query": "PGINTERFACECHOICE",
        }
        super(UserObject, self).__init__(**object)
