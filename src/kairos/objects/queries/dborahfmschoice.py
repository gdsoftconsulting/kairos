null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "DBORAHFMSCHOICE",
            "collections": ["ORAHQS"],
            "request": "select distinct force_matching_signature as label from ORAHQS order by label"
        }
        super(UserObject, self).__init__(**object)
