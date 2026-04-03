from enum import Enum

class UserProfileLoadSTATUS(Enum):
    SUCCESS = 0
    UNAUTH = 1
    DBNOPROFILE = 2


class GameApiReturnSTATUS(Enum):
    SUCCESS = 0
    R_NOCONNECTION = 1
    R_TIMEOUT = 2
    R_UNKNOWN = 3

    API_INVALIDAPIKEY = 4
    API_MISSINGVALUE = 5
    API_UNKNOWN = 6
