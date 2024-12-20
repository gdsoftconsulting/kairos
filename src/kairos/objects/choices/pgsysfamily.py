class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "PGSYSFAMILY",
            "action": "dispchart",
            "chart": "PGSYSCHOOSEFAMILY",
            "query": "PGFAMILYCHOICE",
        }
        super(UserObject, self).__init__(**object)
