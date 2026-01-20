from dataflow import get_nations_data, get_wars_data, extract_nationSet

if __name__ == "__main__":
    allianceSet = {4221}
    wars = get_wars_data(allianceSet)
    
    nationSet = extract_nationSet(wars)
    nations = get_nations_data(nationSet)

