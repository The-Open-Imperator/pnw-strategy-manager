from dash import dash_table

def wartable_name_id_mapping():
    m = [
            {'name':['atk','☎️'], 'id': 'a_discord'},
            {'name':['atk', '🏗'], 'id': 'a_cities'},
            {'name':['atk', '🚢'], 'id': 'a_ships'},
            {'name':['atk', '✈'], 'id': 'a_aircraft'},
            {'name':['atk', '⚙'], 'id': 'a_tanks'},
            {'name':['atk', '💂'], 'id': 'a_soldiers'},
            {'name':['atk', '🌐'], 'id': 'a_alliance'},
            {'name':['atk', 'Name'], 'id': 'a_nation_name'},
            {'name':['atk', 'RES'], 'id': 'a_resistance'},
            {'name':['atk', 'MAP'], 'id': 'a_MAP'},

            {'name':['', '🕛'], 'id': 'turns_left'},

            {'name':['def', 'MAP'], 'id': 'd_MAP'},
            {'name':['def', 'RES'], 'id': 'd_resistance'},
            {'name':['def', 'Name'], 'id': 'd_nation_name'},
            {'name':['def', '🌐'], 'id': 'd_alliance'},
            {'name':['def', '💂'], 'id': 'd_soldiers'},
            {'name':['def', '⚙'], 'id': 'd_tanks'},
            {'name':['def', '✈'], 'id': 'd_aircraft'},
            {'name':['def', '🚢'], 'id': 'd_ships'},
            {'name':['def', '🏗'], 'id': 'd_cities'},
            {'name':['def', '☎️'], 'id': 'd_discord'}
            ]
    return m

def wartable_cell_conditional():
    cond = list()
    for c in ['d_MAP', 'd_resistance', 'd_nation_name', 'd_alliance', 'd_soldiers', 'd_tanks', 'd_aircraft', 'd_ships', 'd_cities', 'd_discord']:
        cond.append({'if': {'column_id': c}, 'textAlign':'left'})

    cond.append({'if': {'column_id': 'turns_left'}, 'textAlign':'center'})
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




