import requests
import json
import os

from utils import DEFAULT_NO_ALLIANCE

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

def get_nations_data(nationSet: set):
    data = requests.post(URL, json={"query": nationsQuery.replace("NATIONS", str(list(nationSet)))})
    data = json.loads(data.content)
    return data["data"]["nations"]["data"]

def get_wars_data(allianceSet: set):
    data = requests.post(URL, json={"query": warsQuery.replace("ALLIANCES", str(list(allianceSet)))})
    data = json.loads(data.content)
    return data["data"]["wars"]["data"]

def get_member_nation_data(allianceSet: set):
    data = requests.post(URL, json={"query": allianceQuery.replace("ALLIANCES", str(list(allianceSet)))})
    data = json.loads(data.content)
    return data["data"]["alliances"]["data"]

def extract_nationSet(warList: list) -> set:
    nationSet = set()
    for war in warList:
        nationSet.add(int(war["att_id"]))
        nationSet.add(int(war["def_id"]))
    return nationSet

def nations_to_dict(nationList: list) -> dict:
    d = dict()

    for nation in nationList:
        if nation['alliance'] == None:
            nation['alliance'] = DEFAULT_NO_ALLIANCE
        d[nation["id"]] = nation

    return d

def init_wars_nations_from_allianceSet(allianceSet: set) -> (list, dict):
    wars = get_wars_data(allianceSet)
    nations = get_nations_data(extract_nationSet(wars))
    nations = nations_to_dict(nations)

    return (wars, nations)


def extract_nations_from_allianceList(allianceList: list, excludeFilter: dict) -> list:
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

def init_nations_from_allianceSet(allianceSet: set, excludeFilter: dict) -> list:
    allianceList = get_member_nation_data(allianceSet)
    nations = extract_nations_from_allianceList(allianceList, excludeFilter)
    return nations

if __name__=="__main__":
    allianceSet = {4221}
    wars, nations = init_wars_nations_from_allianceSet(allianceSet)
    print(f"Retrived {len(wars)} war and {len(nations)} nation data entries")
    #print(nations)


    from utils import DEFAULT_NATION_FILTER
    allianceSet = {14548, 14750}
    nations = init_nations_from_allianceSet(allianceSet, DEFAULT_NATION_FILTER)
    print(f"Retrived {len(nations)} nation entries from allianceSet: {allianceSet}")
