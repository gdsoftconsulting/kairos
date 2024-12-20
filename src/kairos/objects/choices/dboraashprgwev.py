class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHPRGWEV",
            "action": "dispchart",
            "chart": "DBORAASHPRGWEV",
            "query": "DBORAASHPRGCHOICE",
        }
        super(UserObject, self).__init__(**object)
