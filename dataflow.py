import requests
import json
import os

import logging
logger = logging.getLogger("MAINLOG")

from utils import DEFAULT_NO_ALLIANCE
from errorstates import GameApiReturnSTATUS

KEY=os.getenv("APIKEY")
URL = 'https://api.politicsandwar.com/graphql?api_key=' + KEY

nationsQuery= """{nations(id: NATIONS, first:500)
  {
    data
    {
      id
      nation_name
      discord
      discord_id
      beige_turns
      alliance { name, id }
      score
      num_cities
      soldiers
      tanks
      aircraft
      ships
      missiles
      nukes
    }
    
  }
}"""

warsQuery= """{wars(alliance_id: ALLIANCES, active: true, first: 500)
  {
    data
    {
      id
      turns_left
      att_id
      att_alliance_id
      att_alliance_position
      att_resistance
      att_points
      def_id
      def_alliance_id
      def_alliance_position
      def_resistance
      def_points
      
    }
    
  }
}
"""

allianceQuery = """{alliances(id: ALLIANCES)
  {
    data
    {
      nations{
            id
            nation_name
            alliance { name, id }
            alliance_position
            last_active
            score
            num_cities
            color
            beige_turns
            vacation_mode_turns
            offensive_wars_count
            defensive_wars_count
            soldiers
            tanks
            aircraft
            ships
            missiles
            nukes
            spies

      }
      
    }
    
  }
}
"""

homepageAllianceQuery = """{alliances(id: ALLIANCE)
  {
    data
    {
      id
      name
      score
      rank
      color
      flag
      nations{
        color
        last_active
        vacation_mode_turns
        num_cities
        war_policy
        domestic_policy
      }
      wars{
        att_alliance_id
        def_alliance_id
        war_type
      }
    }
    
  }
}
"""

def get_nations_data(nationSet: set):
    data = requests.post(URL, json={"query": nationsQuery.replace("NATIONS", str(list(nationSet)))})
    data = json.loads(data.content)
    return data

def get_wars_data(allianceSet: set):
    data = requests.post(URL, json={"query": warsQuery.replace("ALLIANCES", str(list(allianceSet)))})
    data = json.loads(data.content)
    return data

def get_member_nation_data(allianceSet: set):
    data = requests.post(URL, json={"query": allianceQuery.replace("ALLIANCES", str(list(allianceSet)))})
    data = json.loads(data.content)
    return data

def get_alliance_stats(allianceSet: set):
    data = requests.post(URL, json={"query": homepageAllianceQuery.replace("ALLIANCE", str(list(allianceSet)))})
    data = json.loads(data.content)
    return data["data"]["alliances"]["data"][0]

class GameDataClass():
    # FUNC: _requests_validation
    # DESC: Executes the func function and catches requests exceptions. Also checks if the api returned an error.
    #           ON ERROR: self.status contains an enum with not 0 as value
    #           ON SUCCESS: self.status contains an enum with 0 as value
    # RETURN: The requested json list of game data
    def _requests_validation(self, func, dataIN: set):
        try:
            dataOUT = func(dataIN)
        except requests.exceptions.Timeout:
            self.status = GameApiReturnSTATUS.R_TIMEOUT
            return 
        except requests.exceptions.ConnectionError:
            self.status = GameApiReturnSTATUS.R_NOCONNECTION
            return 
        except requests.exceptions.RequestException:
            self.status = GameApiReturnSTATUS.R_UNKNOWN
            return

        # Check for data validity and set GameApiReturnSTATUS to failed if invalid
        err = dataOUT.get('errors')
        if err != None:
            msg = err[0].get('message') 
            if msg == 'You specified an invalid api_key. Your URL should like this: https://api.politicsandwar.com/graphql?api_key=xxx':
                self.status = GameApiReturnSTATUS.API_INVALIDAPIKEY
                return 
            else:
                self.status = GameApiReturnSTATUS.API_UNKNOWN
                return
        self.status = GameApiReturnSTATUS.SUCCESS
        return dataOUT


class NationsFromAAIDSet(GameDataClass):
    # FUNC: _apply_filter_on_AAList
    # DESC: Filters a set of data elements with the structure allianceList = { alliances { nations { nationDATA }}}.
    def _apply_filter_on_AAList(self, allianceList: set, excludeFilter: dict) -> list:
        l = list()

        for alliance in allianceList:
            for nation in alliance["nations"]:
                # Apply filter
                if (excludeFilter['excludeApplicants'] and nation['alliance_position'] == 'APPLICANT'):
                    continue
                if (excludeFilter['excludeBeige'] and nation['beige_turns'] > excludeFilter['includeIfBeigeLessThan']):
                    continue
                if (excludeFilter['excludeVacation'] and nation['vacation_mode_turns'] > excludeFilter['includeIfVacationLessThan']):
                    continue
                if (excludeFilter['excludeNoDefSlot'] and nation['defensive_wars_count'] > 2):
                    continue
                if (excludeFilter['excludeNoOffSlot'] and nation['offensive_wars_count'] > 4):
                    continue

                #Alliance field None fix
                if nation['alliance'] == None:
                    nation['alliance'] = ""
                else:
                    nation['alliance'] = nation['alliance']['name']
                l.append(nation)

        return l

    def __init__(self, allianceIDSet: set, excludeFilter: dict):
        # Check if requests worked
        dataOUT = self._requests_validation(get_member_nation_data, allianceIDSet)
        if (self.status.value):
            return

        # Check for data validity. MUST BE data = dataOUT['data']['alliances']['data']
        data = dataOUT.get("data")
        if (data == None):
            self.status = GameApiReturnSTATUS.API_MISSINGVALUE
            return
        data = data.get("alliances")
        if (data == None):
            self.status = GameApiReturnSTATUS.API_MISSINGVALUE
            return
        data = data.get("data")
        if (data == None):
            self.status = GameApiReturnSTATUS.API_MISSINGVALUE
            return

        self.nations = self._apply_filter_on_AAList(data, excludeFilter)
        self.status = GameApiReturnSTATUS.SUCCESS

class WarsNationsFromAAIDSet(GameDataClass):
    def _extract_nationSet(self, warList: list) -> set:
        nationSet = set()
        for war in warList:
            nationSet.add(int(war["att_id"]))
            nationSet.add(int(war["def_id"]))
        return nationSet

    def _nations_to_dict(self, nationList: list) -> dict:
        d = dict()

        for nation in nationList:
            if nation['alliance'] == None:
                nation['alliance'] = DEFAULT_NO_ALLIANCE
            d[nation["id"]] = nation
        return d

    def __init__(self, allianceSet: set):
        # Check if requests worked
        dataOUT = self._requests_validation(get_wars_data, allianceSet)
        if (self.status.value):
            return

        # Check for data validity. MUST BE data = dataOUT['data']['wars']['data']
        data = dataOUT.get('data')
        if (data == None):
            self.status = GameApiReturnSTATUS.API_MISSINGVALUE
            return
        data = data.get('wars')
        if (data == None):
            self.status = GameApiReturnSTATUS.API_MISSINGVALUE
            return
        self.wars = data.get('data')
        if (self.wars == None):
            self.status = GameApiReturnSTATUS.API_MISSINGVALUE
            return
        
        # Check if requests worked
        dataOUT = self._requests_validation(get_nations_data, self._extract_nationSet(self.wars))
        if (self.status.value):
            return

        # Check for data validity. MUST BE data = dataOUT['data']['nations']['data']
        data = dataOUT.get('data')
        if (data == None):
            self.status = GameApiReturnSTATUS.API_MISSINGVALUE
            return
        data = data.get('nations')
        if (data == None):
            self.status = GameApiReturnSTATUS.API_MISSINGVALUE
            return
        nationList = data.get('data')
        if (nationList == None):
            self.status = GameApiReturnSTATUS.API_MISSINGVALUE
            return

        self.nations = self._nations_to_dict(nationList)
        self.status = GameApiReturnSTATUS.SUCCESS


if __name__=="__main__":
    allianceSet = {4221}
    wnDat = WarsNationsFromAAIDSet(allianceSet)
    if (wnDat.status.value):
        print(f"ERR_{wnDat.status}")
    else:
        print(f"Retrived {len(wnDat.wars)} war and {len(wnDat.nations)} nation data entries")


    from utils import DEFAULT_NATION_FILTER
    allianceSet = {4221, 5476}
    nationDat = NationsFromAAIDSet(allianceSet, DEFAULT_NATION_FILTER)
    if (nationDat.status.value):
        print(f"ERR_{nationDat.status}")
    else:
        print(f"Retrived {len(nationDat.nations)} nation entries from allianceSet: {allianceSet}")
