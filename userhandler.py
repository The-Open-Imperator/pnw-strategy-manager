from flask import request


def get_username():
    return request.authorization['username']



class UserData:
    def __init__(self):
        self.username = get_username()
        self.role = "root"
        self.title = "Operational Strategist"
        self.alliance = 4221
        self.nationID = 190029
