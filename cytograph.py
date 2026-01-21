import dash_cytoscape as cyto

def create_element_list(wars: list, nations: dict) -> list:
    elements = list()

    for ID, nation in nations.items():
        if nation["alliance"] != None:
            if nation["alliance"]["name"] == "Spectre":
                elements.append( {'data': {'id':ID, 'label':ID}, 'classes':'blue'})
            else:
                elements.append( {'data': {'id':ID, 'label':ID}, 'classes':'red'})
        else:
            elements.append( {'data': {'id':ID, 'label':ID}})
                
    for war in wars:
        elements.append( {'data': {'source':war['att_id'], 'target':war['def_id']}})
    return elements

def dash_cyto_format(wars: list, nations: dict):
    cy = cyto.Cytoscape(
        layout={'name': 'cose'},
        style={'width':'100%', 'height':'1500px'},
        elements=create_element_list(wars, nations),
        stylesheet=[
            # Group selectors
            {
                'selector': 'node',
                'style': {
                    'content': 'data(label)'
                }
            },

            # Class selectors
            {
                'selector': '.red',
                'style': {
                    'background-color': 'red',
                    'line-color': 'red'
                }
            },
            # Class selectors
            {
                'selector': '.blue',
                'style': {
                    'background-color': 'blue',
                    'line-color': 'blue'
                }
            },
            {
                'selector': '.triangle',
                'style': {
                    'shape': 'triangle'
                }
            }])
    return cy
