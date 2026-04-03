from flask import request

from errorstates import UserProfileLoadSTATUS

import logging
logger = logging.getLogger("MAINLOG")

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
    if db_connector.fetch_username_password_raw(username, password) == None:
        return False
    else:
        return True
        

class UserData:
    def __init__(self):
        self.username = get_username()
        if self.username == None:
            logger.error("userhandler.UserData -> tried to load user profile for an unauthenticaed user!")
            self.status = UserProfileLoadSTATUS.UNAUTH
            return

        userprofile = db_connector.fetch_userprofile_raw(self.username)
        if userprofile == None:
            logger.error(f"userhandler.UserData -> db returned no user profile for user={self.username}!")
            self.status = UserProfileLoadSTATUS.DBNOPROFILE
            return
        self.userid = userprofile[0]
        #self.username = userprofile[1]
        self.nationid = userprofile[2]
        self.allianceid = userprofile[3]
        self.title = userprofile[4]

        self.status = UserProfileLoadSTATUS.SUCCESS
