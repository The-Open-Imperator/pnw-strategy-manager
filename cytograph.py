import dash_cytoscape as cyto
from graphs import Sphere, Graph

left = -500
right = 500
space = 75

nodeHeight = 50
nodeWidth = 350


def create_element_list(wars: list, nations: dict) -> list:
    G = Graph(nations, wars)
    G.add_from_nations_wars(wars, nations)

    G.generate_layout()
    
    print(G.get_all())
    return G.get_all()

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
