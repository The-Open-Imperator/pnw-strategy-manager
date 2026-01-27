import requests
import json
import os

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

warsQuery= """{wars(alliance_id: ALLIANCES, active: true, first: 200)
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

def get_nations_data(nationSet: set):
    data = requests.post(URL, json={"query": nationsQuery.replace("NATIONS", str(list(nationSet)))})
    data = json.loads(data.content)
    return data["data"]["nations"]["data"]

def get_wars_data(allianceSet: set):
    data = requests.post(URL, json={"query": warsQuery.replace("ALLIANCES", str(list(allianceSet)))})
    data = json.loads(data.content)
    return data["data"]["wars"]["data"]


def extract_nationSet(warList: list) -> set:
    nationSet = set()
    for war in warList:
        nationSet.add(int(war["att_id"]))
        nationSet.add(int(war["def_id"]))
    return nationSet

def nations_to_dict(nationList: list) -> dict:
    d = dict()

    for nation in nationList:
        d[nation["id"]] = nation

    return d


def init_wars_nations_from_allianceSet(allianceSet: set) -> (list, dict):
    wars = get_wars_data(allianceSet)
    nations = get_nations_data(extract_nationSet(wars))
    nations = nations_to_dict(nations)

    return (wars, nations)


if __name__=="__main__":
    allianceSet = {4221}
    wars, nations = init_wars_nations_from_allianceSet(allianceSet)

    print(nations)
