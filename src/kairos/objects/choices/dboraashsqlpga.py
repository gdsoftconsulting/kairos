class UserObject(dict):
    def __init__(self):
        object = {
            "type": "choice",
            "id": "DBORAASHSQLPGA",
            "action": "dispchart",
            "chart": "DBORAASHSQLPGA",
            "query": "DBORAASHSQLCHOICE",
        }
        super(UserObject, self).__init__(**object)
