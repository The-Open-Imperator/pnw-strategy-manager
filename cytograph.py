import dash_cytoscape as cyto
from graphs import Sphere

left = -500
right = 500
space = 75

nodeHeight = 50
nodeWidth = 350


def make_label(nation: dict) -> str:
    return f"{nation['nation_name']} | c:{nation['num_cities']} | s:{nation['score']} \n s:{nation['soldiers']} | t:{nation['tanks']} | a:{nation['aircraft']} | s:{nation['ships']}"

def add_node(nation: dict) -> dict:
    node = dict()
    node['data'] = {'id': nation['id'], 'label': make_label(nation)}
    node['type'] = 'node'

    # Group attributes to color the nodes with stylesheet
    node['data']['group'] = Sphere.map_alliance_to_sphere(nation.get('alliance'))
    
    return node

def add_edge(war: dict) -> dict:
    edge = dict()
    label = f"a:{war['att_resistance']} | {war['turns_left']} | d:{war['def_resistance']}"
    edge['data'] = {'source':war['att_id'], 'target':war['def_id'], 'label': label}
    
    edge['type'] = 'edge' 
    edge['data']['group'] = Sphere.map_allianceID_to_sphere(war['att_alliance_id'])
    print(edge)
    return edge

def set_node_positions(nodes: list, edges: list) -> list:
    NnodeLeftUp = 0
    NnodeLeftDown = 0
    NnodeRightUp = 0
    NnodeRightDown = 0

    for n in nodes:
        if n['type'] == 'edge':   # Check if object is a node
            continue

        g = n['data']['group'] 
        if g == Sphere.ALLIANCE or g == Sphere.SPHERE:
            x = left
            y = NnodeLeftUp
            NnodeLeftUp += 1
        else:
            x = right
            y = NnodeRightUp
            NnodeRightUp += 1

        n['position'] = {'x': x, 'y': y*space}
    return nodes

def create_element_list(wars: list, nations: dict) -> list:
    nodes = list()
    edges = list()

    for ID, nation in nations.items():
        nodes.append(add_node(nation))

    for war in wars:
        edges.append(add_edge(war))
    
    nodes = set_node_positions(nodes, edges)

    return nodes + edges 

def calc_graph_height(nations: int) -> int:
    return space * nations + nodeHeight * nations

def calc_graph_width() -> int:
    return 2* nodeWidth - left + right

def dash_cyto_format(wars: list, nations: dict):
    height = calc_graph_height(len(nations))
    width = calc_graph_width()

    cy = cyto.Cytoscape(
        zoom = 1,
        userZoomingEnabled = False,
        layout={'name': 'preset',
                'fit': False
            },
        style={'width':f'{width}', 
               'height':f'{height}px'
            },
        pan = {'x': width, 'y': int(height / 6)},
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
                    #'mid-target-arrow-shape': 'triangle',
                    'curve-style': 'unbundled-bezier',
                    #'control-point-ditances': '0.2 0.5 0.8',
                    #'control-point-weight': '1 0 1',
                    'label': 'data(label)',
                    'text-margin-y': '-20'
                }
            },

            # Class selectors
            {
                'selector': f"node[group = '{Sphere.ALLIANCE}']",
                'style': {
                    'border-color': 'blue'
                    #'line-color': 'blue'
                }
            },
            # Class selectors
            {
                'selector': f"node[group = '{Sphere.SPHERE}']",
                'style': {
                    'border-color': 'aqua'
                    #'line-color': 'aqua'
                }
            },
            # Class selector
            {
                'selector': f"node[group = '{Sphere.UNALLIED}']",
                'style': {
                    'border-color':'grey'
                    #'line-color': 'grey'
                }
            },
            # Class selector
            {
                'selector': f"node[group = '{Sphere.ENEMY}']",
                'style': {
                    #'line-color': 'red'
                    'border-color': 'red'
                }
            },
            # Edge electors
            {
                'selector': f"edge[group = '{Sphere.ALLIANCE}']",
                'style': {
                    'source-endpoint': '50% 0%',
                    'target-endpoint': '-50% 0%',
                    'line-color': 'blue'
                }
            },
            # Edge selectors
            {
                'selector': f"edge[group = '{Sphere.SPHERE}']",
                'style': {
                    'source-endpoint': '50% 0%',
                    'target-endpoint': '-50% 0%',
                    'line-color': 'aqua'
                }
            },
            # Edge selector
            {
                'selector': f"edge[group = '{Sphere.UNALLIED}']",
                'style': {
                    'source-endpoint': '-50% 0%',
                    'target-endpoint': '50% 0%'
                }

            },
            # Edge selector
            {
                'selector': f"edge[group = '{Sphere.ENEMY}']",
                'style': {
                    'source-endpoint': '-50% 0%',
                    'target-endpoint': '50% 0%'
                }
            }])
    return cy
