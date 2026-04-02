from flask import request

import logging
logger = logging.getLogger(__name__)

import db_connector

# NAME: userhandler.py
# DECS: Provides info about the authenticated user.


# FUNC: get_username
# DESC: returns None for unauthenticated users or the username. 
def get_username():
    if request.authorization == None:
        return None
    return request.authorization['username']


def is_valid_username_password(username: str, password: str):
    if db_connector.select_username_password(username, password) == None:
        return False
    else:
        return True
        

class UserData:
    def __init__(self):
        self.username = get_username()
        if self.username == None:
            logger.error("userhandler.UserData -> tried to load user profile for an unauthenticaed user!")
            self.failed = True
            return

        userprofile = db_connector.get_userprofile(self.username)
        if userprofile == None:
            logger.error("userhandler.UserData -> db returned no user profile for an authenticated user!")
            self.failed = True
            return
        self.userid = userprofile[0]
        #self.username = userprofile[1]
        self.nationid = userprofile[2]
        self.allianceid = userprofile[3]
        self.title = userprofile[4]

        self.failed = False
