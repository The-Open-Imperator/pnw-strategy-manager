from flask import request

import logging
logger = logging.getLogger(__name__)

# NAME: userhandler.py
# DECS: Provides info about the authenticated user.


# FUNC: get_username
# DESC: returns None for unauthenticated users or the username. 
def get_username():
    if request.authorization == None:
        return None
    return request.authorization['username']



class UserData:
    def __init__(self):
        self.username = get_username()
        if self.username == None:
            logger.error("userhandler -> tried to load user profile for an unauthenticaed user!")
            return

        self.role = "root"
        self.title = "Operational Strategist"
        self.alliance = 4221
        self.nationID = 190029
