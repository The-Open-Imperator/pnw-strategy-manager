import dash_cytoscape as cyto

sphereList = ["World Task Force", "SFR Yugoslavia", "Dark Brotherhood", "Farkistan"]

def add_node(nation: dict) -> dict:
    node = dict()
    label = f"{nation['nation_name']} | c:{nation['num_cities']} | s:{nation['score']} \n s:{nation['soldiers']} | t:{nation['tanks']} | a:{nation['aircraft']} | s:{nation['ships']}"
    node['data'] = {'id': nation['id'], 'label': label}

    if nation["alliance"] != None:
        if nation["alliance"]["name"] == "Spectre":
            node['data']['group'] = 'alliance'
        elif nation["alliance"]["name"] in sphereList:
            node['data']['group'] = 'sphere'
        else: 
            node['data']['group'] = 'enemy'
    else:
        node['classes'] = 'unallied'
    
    print(node)
    return node

def add_edge(war: dict) -> dict:
    edge = dict()
    label = f"a:{war['att_resistance']} | {war['turns_left']} | d:{war['def_resistance']}"
    edge['data'] = {'source':war['att_id'], 'target':war['def_id'], 'label': label}

    return edge

def create_element_list(wars: list, nations: dict) -> list:
    elements = list()

    for ID, nation in nations.items():
        elements.append(add_node(nation))

    for war in wars:
        elements.append(add_edge(war))

    return elements

def dash_cyto_format(wars: list, nations: dict):
    cy = cyto.Cytoscape(
        layout={'name': 'cose'},
        style={'width':'100%', 'height':'1500px'},
        elements=create_element_list(wars, nations),
        stylesheet=[
            # All nodes selector
            {
                'selector': 'node',
                'style': {
                    'content': 'data(label)',
                    'text-wrap': 'wrap',
                    'text-size': '22',
                    'shape': 'round-rectangle',
                    'width': '350px',
                    'height': '50px',
                    'text-halign': 'center',
                    'text-valign': 'center',
                    'border-width': '3',
                    'background-color': 'white'

                }
            },
            # All edges
            {
                'selector': 'edge',
                'style': {
                    'mid-target-arrow-shape': 'triangle',
                    'label': 'data(label)',
                    'text-margin-y': '-20'
                }
            },

            # Class selectors
            {
                'selector': 'node[group = "alliance"]',
                'style': {
                    'border-color': 'blue'
                    #'line-color': 'blue'
                }
            },
            # Class selectors
            {
                'selector': 'node[group = "sphere"]',
                'style': {
                    'border-color': 'aqua'
                    #'line-color': 'aqua'
                }
            },
            # Class selector
            {
                'selector': 'node[group = "unallied"]',
                'style': {
                    'border-color':'grey'
                    #'line-color': 'grey'
                }
            },
            # Class selector
            {
                'selector': 'node[group = "enemy"]',
                'style': {
                    #'line-color': 'red'
                    'border-color': 'red'
                }
            }])
    return cy
