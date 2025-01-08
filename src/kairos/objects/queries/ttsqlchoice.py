null=None
true=True
false=False

class UserObject(dict):
    def __init__(self):
        object = {
            "type": "query",
            "id": "TTSQLCHOICE",
            "collections": ["TTSQLHS"],
            "request": "select distinct hashid as label from TTSQLHS order by label"
        }
        super(UserObject, self).__init__(**object)
