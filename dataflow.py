import requests
import json
import os

KEY=os.getenv("APIKEY")
URL = 'https://api.politicsandwar.com/graphql?api_key=' + KEY

nationsQuery= """{nations(id: NATIONS)
  {
    data
    {
      id
      nation_name
      alliance { name }
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
      att_id
      att_resistance
      att_points
      def_id
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


def extract_nationSet(warList) -> set:
    nationSet = set()
    for war in warList:
        nationSet.add(int(war["att_id"]))
        nationSet.add(int(war["def_id"]))
    return nationSet
