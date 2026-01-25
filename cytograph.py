import dash_cytoscape as cyto
from graphs import Sphere, Graph

class Viewport:
    nodePosLeft = 350
    nodePosRight = 1350
    nodeSpace = 75

    nodeHeight = 50
    nodeWidth = 350

    warNodeHeight = 25
    warNodeWidth = 250


def create_element_list(wars: list, nations: dict) -> (list, int):
    G = Graph(wars, nations)
    maxNodesInCol = G.generate_layout(Viewport.nodePosLeft, Viewport.nodePosRight, Viewport.nodeSpace)
    
    return (G.get_all(), maxNodesInCol)

def calc_graph_height(maxNodesInCol: int) -> int:
    return maxNodesInCol * (Viewport.nodeSpace + Viewport.nodeWidth)

def dash_cyto_format(wars: list, nations: dict):
    elements, maxNodesInCol = create_element_list(wars, nations) 
    height = calc_graph_height(maxNodesInCol)

    cy = cyto.Cytoscape(
        zoom = 1,
        userZoomingEnabled = False,
        layout={'name': 'preset',
                'fit': False,
                'avoidOverlap': True
            },
        style={'width':'100%', 
               'height':f'{height}px'
            },
        pan = {'x': 0, 'y': 300},
        elements=elements,
        stylesheet=[
            # All nodes selector
            {
                'selector': 'node',
                'style': {
                    'content': 'data(label)',
                    'text-wrap': 'wrap',
                    'text-size': '22',
                    'shape': 'round-rectangle',
                    'width': f'{Viewport.nodeWidth}px',
                    'height': f'{Viewport.nodeHeight}px',
                    'text-halign': 'center',
                    'text-valign': 'center',
                    'border-width': '3',
                    'background-color': 'white'

                }
            },
            # All warnodes
            {
                'selector': "node[type = 'warnode']",
                'style': {
                        'content': 'data(label)',
                        'text-size': '18',
                        'width': f'{Viewport.warNodeWidth}px',
                        'height': f'{Viewport.warNodeHeight}px'
                    }
            },

            # All edges
            {
                'selector': 'edge',
                'style': {
                    #'mid-target-arrow-shape': 'triangle',
                    #'curve-style': 'unbundled-bezier',
                    'curve-style': 'straight',
                    #'control-point-ditances': '0.2 0.5 0.8',
                    #'control-point-weight': '1 0 1',
                }
            },

            # Class selectors
            {
                'selector': f"node[group = '{Sphere.ALLIANCE}']",
                'style': {
                    'border-color': 'grey',
                    'background-fill' : 'linear-gradient',
                    'background-gradient-stop-colors': 'white blue',
                    'background-gradient-stop-positions' : '80% 100%'
                    #'line-color': 'blue'
                }
            },
            # Class selectors
            {
                'selector': f"node[group = '{Sphere.SPHERE}']",
                'style': {
                    'border-color': 'grey',
                    'background-fill' : 'linear-gradient',
                    'background-gradient-stop-colors': 'white aqua',
                    'background-gradient-stop-positions' : '80% 100%'
                    #'line-color': 'aqua'
                }
            },
            # Class selector
            {
                'selector': f"node[group = '{Sphere.UNALLIED}']",
                'style': {
                    'border-color': 'grey',
                    'background-fill' : 'linear-gradient',
                    'background-gradient-stop-colors': 'white gray',
                    'background-gradient-stop-positions' : '80% 100%'
                    #'line-color': 'grey'
                }
            },
            # Class selector
            {
                'selector': f"node[group = '{Sphere.ENEMY}']",
                'style': {
                    'border-color': 'grey',
                    'background-fill' : 'linear-gradient',
                    'background-gradient-stop-colors': 'white red',
                    'background-gradient-stop-positions' : '80% 100%'
                }
            },
            # Edge electors
            {
                'selector': f"edge[type = 'edge-sw']",
                'style': {
                    'source-endpoint': '50% 0%',
                    'target-endpoint': '-50% 0%',
                    'line-color': 'blue'
                }
            },
            # Edge selectors
            {
                'selector': f"edge[type = 'edge-we']",
                'style': {
                    'source-endpoint': '50% 0%',
                    'target-endpoint': '-50% 0%',
                    'line-color': 'blue'
                }
            },
            # Edge selector
            {
                'selector': f"edge[type = 'edge-ws']",
                'style': {
                    'source-endpoint': '-50% 0%',
                    'target-endpoint': '50% 0%',
                    'line-color': 'red'
                }

            },
            # Edge selector
            {
                'selector': f"edge[type = 'edge-ew']",
                'style': {
                    'source-endpoint': '-50% 0%',
                    'target-endpoint': '50% 0%',
                    'line-color': 'red'
                }
            }])
    return cy
