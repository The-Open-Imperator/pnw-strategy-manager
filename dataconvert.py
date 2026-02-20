import pandas as pd

from utils import DEFAULT_NO_ALLIANCE, DEFAULT_WAR_POLICIES_DICT, DEFAULT_DOMESTIC_POLICIES_DICT, DEFAULT_COLORS_DICT, DEFAULT_WAR_TYPES_DICT

from dataflow import get_alliance_stats

class AllianceStats():
    def __init__(self, allianceID: int):
        self._pull_and_convert(allianceID)

    def _pull_and_convert(self, allianceID: int):
        data = get_alliance_stats(allianceID)
        self.id = data["id"]
        self.name = data["name"]
        self.score = data["score"]
        self.rank = data["rank"]
        self.color = data["color"]
        self.flag = data["flag"]

        self._calc_nations_data(data["nations"])
        self._calc_wars_data(data["wars"])

    """
    DESC:
        Computes nation dependent statistics
    ARGS:
        nations: list of nation dicts containing {color, last_active, vacation_mode_turns, num_cities, war_policy, domestic_policy}
    VALUES:
        dict: sum_colors as color:count
        int: sum_nations active in last 24hrs
        int: sum_nations active in last 72hrs
        int: sum_cities
        dict: sum_war_policies as policy:count
        dict: sum_domestic_policies as policy:count
        dict: cityDistribution as numCities:count
    """
    def _calc_nations_data(self, nations: list):
        self.sumColors = dict(DEFAULT_COLORS_DICT)
        self.sumWarPolicies = dict(DEFAULT_WAR_POLICIES_DICT)
        self.sumDomesticPolicies = dict(DEFAULT_DOMESTIC_POLICIES_DICT)
        self.cityDistribution = dict()
        self.sumNationActive_24 = 0
        self.sumNationActive_72 = 0
        self.sumCities = 0
        self.sumMembers = 0

        for n in nations:
            if (n['vacation_mode_turns'] > 0):
                continue

            if (self.cityDistribution.get(n['num_cities']) == None):        # No member with num_cities in dict yet
                self.cityDistribution[n['num_cities']] = 1
            else:
                self.cityDistribution[n['num_cities']] += 1

            # DO time calc later
            self.sumMembers += 1
            self.sumCities += n['num_cities']
            self.sumColors[n['color']] += 1
            self.sumWarPolicies[n['war_policy']] += 1
            self.sumDomesticPolicies[n['domestic_policy']] += 1
    """
    DESC:
        Computes war dependent statistics
    ARGS: 
        wars: list of war dicts containing {att_alliance_id, def_alliance_id, war_type}
    VALUES:
        int: sum_offensive_wars
        int: sum_defensive_wars
        dict: sum_war_types as war_type:count
    """
    def _calc_wars_data(self, wars: list):
        self.sumOffensiveWarTypes = dict(DEFAULT_WAR_TYPES_DICT)
        self.sumDefensiveWarTypes = dict(DEFAULT_WAR_TYPES_DICT)
        self.sumOffensiveWars = 0
        self.sumDefensiveWars = 0

        for w in wars:
            if (w['att_alliance_id'] == self.id):
                self.sumOffensiveWars += 1
                self.sumOffensiveWarTypes[w['war_type']] += 1
            else:
                self.sumDefensiveWars += 1
                self.sumDefensiveWarTypes[w['war_type']] += 1
# END AllianceStats class

def create_warTable_from_wars_nations(wars: list, nations: dict) -> list:
    prelist = []

    for war in wars:
        row = dict()
        atk = nations[war["att_id"]]
        der = nations[war["def_id"]]

        row["a_discord"] = atk["discord"]
        row["a_cities"] = atk["num_cities"]
        row["a_ships"] = atk["ships"]
        row["a_aircraft"] = atk["aircraft"]
        row["a_tanks"] = atk["tanks"]
        row["a_soldiers"] = atk["soldiers"]

        if (atk["alliance"] != None):
            row["a_alliance"] = atk["alliance"]["name"]
        else:
            row["a_alliance"] = DEFAULT_NO_ALLIANCE

        row["a_nation_name"] = atk["nation_name"]
        row["a_resistance"] = war["att_resistance"]
        row["a_MAP"] = war["att_points"]

        row["turns_left"] = war["turns_left"]

        row["d_MAP"] = war["def_points"]
        row["d_resistance"] = war["def_resistance"]
        row["d_nation_name"] = der["nation_name"]
        
        if (der["alliance"] != None):
            row["d_alliance"] = der["alliance"]["name"]
        else:
            row["d_alliance"] = DEFAULT_NO_ALLIANCE

        row["d_soldiers"] = der["soldiers"]
        row["d_tanks"] = der["tanks"]
        row["d_aircraft"] = der["aircraft"]
        row["d_ships"] = der["ships"]
        row["d_cities"] = der["num_cities"]
        row["d_discord"] = der["discord"]

        prelist.append(row)
    return prelist

def csv_str_to_set(allianceList: str) -> set:
    s = set()
    for AA in allianceList.split(','):
        s.add(int(AA))
    return s

if __name__ == '__main__':
    """
    from dataflow import init_wars_nations_from_allianceSet
    allianceSet = {4221}
    wars, nations = init_wars_nations_from_allianceSet(allianceSet)
    dfWarTable = create_warTable_from_wars_nations(wars, nations)
    print(dfWarTable)
    """
    allianceSet = {4221}
    from dataflow import get_alliance_stats
    print(AllianceStats(allianceSet).__dict__)
