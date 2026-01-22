import dash_cytoscape as cyto

left = -500
right = 500
space = 75

nodeHeight = 50
nodeWidth = 350

sphereList = ["World Task Force", "Dark Brotherhood", "Farkistan"]

def make_label(nation: dict) -> str:
    return f"{nation['nation_name']} | c:{nation['num_cities']} | s:{nation['score']} \n s:{nation['soldiers']} | t:{nation['tanks']} | a:{nation['aircraft']} | s:{nation['ships']}"

def add_node(nation: dict) -> dict:
    node = dict()
    node['data'] = {'id': nation['id'], 'label': make_label(nation)}
    node['type'] = 'node'

    # Group attributes to color the nodes with stylesheet
    if nation["alliance"] != None:
        if nation["alliance"]["name"] == "Spectre":
            node['data']['group'] = 'alliance'
        elif nation["alliance"]["name"] in sphereList:
            node['data']['group'] = 'sphere'
        else: 
            node['data']['group'] = 'enemy'
    else:
        node['data']['group'] = 'unallied'
    
    return node

def add_edge(war: dict) -> dict:
    edge = dict()
    label = f"a:{war['att_resistance']} | {war['turns_left']} | d:{war['def_resistance']}"
    edge['data'] = {'source':war['att_id'], 'target':war['def_id'], 'label': label}
    edge['type'] = 'edge'
    return edge

def set_node_positions(elem: list):
    NnodeLeftUp = 0
    NnodeLeftDown = 0
    NnodeRightUp = 0
    NnodeRightDown = 0

    for n in elem:
        if n['type'] == 'edge':   # Check if object is a node
            print("Not a Node")
            continue

        if n['data']['group'] in ["alliance", "sphere"]:
            x = left
            y = NnodeLeftUp
            NnodeLeftUp += 1
        else:
            x = right
            y = NnodeRightUp
            NnodeRightUp += 1

        n['position'] = {'x': x, 'y': y*space}
        print(n)
    return elem

def create_element_list(wars: list, nations: dict) -> list:
    elements = list()

    for ID, nation in nations.items():
        elements.append(add_node(nation))

    for war in wars:
        elements.append(add_edge(war))
    
    elements = set_node_positions(elements)

    return elements

def calc_graph_height(nations: int) -> int:
    return space * nations + nodeHeight * nations

def dash_cyto_format(wars: list, nations: dict):
    height = calc_graph_height(len(nations))
    cy = cyto.Cytoscape(
        zoom = 2,
        userZoomingEnabled = False,
        pan = {'x': 1725, 'y': int(height / 6)},
        layout={'name': 'preset',
                'fit': False
            },
        style={'width':'100%', 
               'height':f'{height}px'
            },
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
                    'width': f'{nodeWidth}px',
                    'height': f'{nodeHeight}px',
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
