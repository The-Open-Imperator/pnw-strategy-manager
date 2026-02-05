from dash import dash_table
from dash.dash_table.Format import Format, Scheme

def wartable_name_id_mapping():
    decimalSI = Format(precision=3, scheme=Scheme.decimal_si_prefix)
    m = [
            {'name':['atk','☎️'], 'id': 'a_discord'},
            {'name':['atk', '🏗'], 'id': 'a_cities'},
            {'name':['atk', '🚢'], 'id': 'a_ships'},
            {'name':['atk', '✈'], 'id': 'a_aircraft'},
            {'name':['atk', '⚙'], 'id': 'a_tanks', 'type':'numeric', 'format':decimalSI},
            {'name':['atk', '💂'], 'id': 'a_soldiers', 'type':'numeric', 'format':decimalSI},
            {'name':['atk', '🌐'], 'id': 'a_alliance'},
            {'name':['atk', 'Name'], 'id': 'a_nation_name'},
            {'name':['atk', 'RES'], 'id': 'a_resistance'},
            {'name':['atk', 'MAP'], 'id': 'a_MAP'},

            {'name':['', '🕛'], 'id': 'turns_left'},

            {'name':['def', 'MAP'], 'id': 'd_MAP'},
            {'name':['def', 'RES'], 'id': 'd_resistance'},
            {'name':['def', 'Name'], 'id': 'd_nation_name'},
            {'name':['def', '🌐'], 'id': 'd_alliance'},
            {'name':['def', '💂'], 'id': 'd_soldiers', 'type':'numeric', 'format':decimalSI},
            {'name':['def', '⚙'], 'id': 'd_tanks', 'type':'numeric', 'format':decimalSI},
            {'name':['def', '✈'], 'id': 'd_aircraft'},
            {'name':['def', '🚢'], 'id': 'd_ships'},
            {'name':['def', '🏗'], 'id': 'd_cities'},
            {'name':['def', '☎️'], 'id': 'd_discord'}
            ]
    return m

def wartable_column_width():
    w = [
            {'id':'a_discord', 'width':'5%'},
            {'id':'a_cities', 'width':'4%'},
            {'id':'a_ships', 'width':'4%'},
            {'id':'a_aircraft', 'width':'4%'},
            {'id':'a_tanks', 'width':'5%'},
            {'id':'a_soldiers', 'width':'5%'},
            {'id':'a_nation_name', 'width':'8%'},
            {'id':'a_resistance', 'width':'3%'},
            {'id':'a_MAP', 'width':'3%'},

            {'id':'turns_left', 'width':'5%'},
            
            {'id':'d_discord', 'width':'5%'},
            {'id':'d_cities', 'width':'4%'},
            {'id':'d_ships', 'width':'4%'},
            {'id':'d_aircraft', 'width':'4%'},
            {'id':'d_tanks', 'width':'5%'},
            {'id':'d_soldiers', 'width':'5%'},
            {'id':'d_nation_name', 'width':'8%'},
            {'id':'d_resistance', 'width':'3%'},
            {'id':'d_MAP', 'width':'3%'}
        ]

    return w

def wartable_cell_conditional():
    cond = list()

    #defender text aligntment left
    for c in ['d_MAP', 'd_resistance', 'd_nation_name', 'd_alliance', 'd_soldiers', 'd_tanks', 'd_aircraft', 'd_ships', 'd_cities', 'd_discord']:
        cond.append({'if': {'column_id': c}, 'textAlign':'left'})

    cond.append({'if': {'column_id': 'turns_left'}, 'textAlign':'center'})

    #column width
    for s in wartable_column_width():
        cond.append({'if': {'column_id':s['id']}, 'width':s['width']})

    return cond

def dash_wartable_format(warTable: list):
    dt = dash_table.DataTable(
        data = warTable,
        columns = wartable_name_id_mapping(),

        # Color every second row darker
        style_data_conditional=[
            {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
            }
        ],
        
        #Headers
        merge_duplicate_headers=True,
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'color': 'black',
            'fontWeight': 'bold',
            'textAlign': 'center'
        },
        
        style_cell_conditional=wartable_cell_conditional(),

        style_cell={
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 0,
            'font-size': '20px'
        },
        

        style_table={
            'border': '3px solid blue',
            'borderRadius': '15px',
            'overflow': 'hidden'
        },

        sort_action='native'
        #row_deletable=True)
        #filter_action='native',
        #filter_options={"placeholder_text": "Filter"})
        )

    return dt




