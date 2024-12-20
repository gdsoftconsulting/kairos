class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHPRGSQL",
            "action": "dispchart",
            "chart": "DBORAASHPRGSQL",
            "query": "DBORAASHPRGCHOICE",
        }
        super(UserObject, self).__init__(**object)
