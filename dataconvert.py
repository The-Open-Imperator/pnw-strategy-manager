import pandas as pd

def create_WarTable_from_wars_nations(wars, nations):
    prelist = []

    for war in wars:
        row = dict()
        atk = nations[war["att_id"]]
        der = nations[war["def_id"]]

        row["a_ships"] = atk["ships"]
        row["a_aircraft"] = atk["aircraft"]
        row["a_tanks"] = atk["tanks"]
        row["a_soldiers"] = atk["soldiers"]
        row["a_cities"] = atk["num_cities"]
        row["a_MAP"] = war["att_points"]
        row["a_resistance"] = war["att_resistance"]
        row["a_nation_name"] = atk["nation_name"]
        row["a_discord"] = atk["discord"]

        if (atk["alliance"] != None):
            row["a_alliance"] = atk["alliance"]["name"]
        else:
            row["a_alliance"] = None

        row["id"] = war["id"]
        row["turns_left"] = war["turns_left"]
    
        row["d_ships"] = der["ships"]
        row["d_aircraft"] = der["aircraft"]
        row["d_tanks"] = der["tanks"]
        row["d_soldiers"] = der["soldiers"]
        row["d_cities"] = der["num_cities"]
        row["d_MAP"] = war["def_points"]
        row["d_resistance"] = war["def_resistance"]
        row["d_nation_name"] = der["nation_name"]
        row["d_discord"] = der["discord"]

        if (der["alliance"] != None):
            row["d_alliance"] = der["alliance"]["name"]
        else:
            row["d_alliance"] = None

        prelist.append(row)

    warTable = pd.DataFrame(prelist)
    return warTable

if __name__ == '__main__':
    from dataflow import init_wars_nations_from_allianceSet
    allianceSet = {4221}
    wars, nations = init_wars_nations_from_allianceSet(allianceSet)
    dfWarTable = create_WarTable_from_wars_nations(wars, nations)
    print(dfWarTable)
