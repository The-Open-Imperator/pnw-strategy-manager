from dash import dash_table

def wartable_cell_conditional():
    cond = list()
    for c in ['d_MAP', 'd_resistance', 'd_nation_name', 'd_alliance', 'd_soldiers', 'd_tanks', 'd_aircraft', 'd_ships', 'd_cities', 'd_discord']:
        cond.append({'if': {'column_id': c}, 'textAlign':'right'})

    cond.append({'if': {'column_id': 'turns_left'}, 'textAlign':'center'})
    return cond

def dash_wartable_format(warTable: list):
    dt = dash_table.DataTable(warTable,
    
    # Color every second row darker
    style_data_conditional=[
        {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(220, 220, 220)',
        }
    ],
    
    style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'color': 'black',
        'fontWeight': 'bold'
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

    sort_action='native',
    row_deletable=True)
    #filter_action='native',
    #filter_options={"placeholder_text": "Filter"})

    return dt




