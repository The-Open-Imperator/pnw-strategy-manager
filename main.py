from dash import Dash, dash_table, html, dcc, callback, Output, Input, State
import dash_cytoscape
import pandas as pd

from wartable import dash_wartable_format, dash_enemytable_format
from cytograph import dash_cyto_format

from dataflow import init_wars_nations_from_allianceSet, init_nations_from_allianceSet
from dataconvert import create_warTable_from_wars_nations, csv_str_to_set

from utils import DEFAULT_NATION_FILTER


nationFilterChecklist = dcc.Checklist(id='filter_enemy_list',
        options=[
                'exclude applicants',
                'exclude beige >2',
                'exclude vacation >2',
                'exclude off slot >4',
                'exclude def slot >2'
            ]
        , 
        value = ['exclude applicants']
                                     )

dataSettings = html.Center(
                    html.Fieldset(children = [
                        html.H3("Data Settings", style={'textAlign':'center', 'font-size':'34'}),
                        
                        html.Div("Get all wars from"),
                        dcc.Input(id='input_alliance_list', type='text', placeholder='AA list, ex: 4221, 1312'),
                        #dcc.Checklist(['Include applicants'], ['Include applicants'], id='include_applicants'),
                        html.Button("Apply & Pull data", id='btn_apply'),
                        
                        html.Div("Get all nations from"),
                        dcc.Input(id='input_enemy_list', type='text', placeholder='AA list, ex: 4221, 1312'),
                        nationFilterChecklist,
                        html.Button("Apply & Pull data", id='btn_apply_enemy')
                                             ],
                                  style = {'width':'400px', 'border-radius':'8px'}
                                )
                          )
 
displaySettings = html.Center(
                        html.Fieldset(children = [
                                        html.H3("Display Settings", style={'textAlign':'center', 'font-size':'34'})
                                                 ],
                                      style = {'width':'400px', 'border-radius':'8px'}
                                     )
                             )

settings = html.Fieldset(children = [
                            html.H2("Settings", style={'textAlign':'center', 'font-size':'38'}),
                            dataSettings,
                            displaySettings
                                    ],
                                    style = {'width':'820px', 'border-radius':'16px'}
                        )

app = Dash()

app.layout = [
    html.H1(children='PnW Strategy Manager', style={'textAlign':'center', 'font-size':'42'}),
    html.Div(html.Center(settings)),
    html.Div(id='enemytable-div', children = []),
    html.Div(id='wartable-div', children = [dash_table.DataTable(id='wartable')]),
    html.Div(id='wargraph-div', children = [])
    ]


@callback(
    Output('wartable-div', 'children'),
    Output('wargraph-div', 'children'),
    Input('btn_apply', 'n_clicks'),
    State('input_alliance_list', 'value'),
    prevent_initial_call=True
)
def update_data(n_clicks, allianceList):
    wars, nations = init_wars_nations_from_allianceSet(csv_str_to_set(allianceList))
    warTable = create_warTable_from_wars_nations(wars, nations)

    return [dash_wartable_format(warTable), dash_cyto_format(wars, nations)]

@callback(
    Output('enemytable-div', 'children'),
    Input('btn_apply_enemy', 'n_clicks'),
    State('input_enemy_list', 'value'),
    State('filter_enemy_list', 'value'),
    prevent_initial_call=True
)
def update_enemytable(n_clicks, allianceList, filter_list):
    excludeFilter = dict(DEFAULT_NATION_FILTER)

    # Setup filter
    if ('exclude applicants' in filter_list):
        excludeFilter['excludeApplicants'] = True
    if ('exclude beige >2' in filter_list):
        excludeFilter['excludeBeige'] = True
    if ('exclude vacation >2' in filter_list):
        excludeFilter['excludeVacation'] = True
    if ('exclude off slot >4' in filter_list):
        excludeFilter['excludeNoOffSlot'] = True
    if ('exclude def slot >2' in filter_list):
        excludeFilter['excludeNoDefSlot'] = True

    nations = init_nations_from_allianceSet(csv_str_to_set(allianceList), excludeFilter)
    
    return [dash_enemytable_format(nations)]


"""
@callback(    
      Output("wartable", "style_data_conditional"),
      Input("wartable", "active_cell"),    
      prevent_initial_call=True
)
def render_content(active_cell):
    style = WartableFormat.style_data_conditional.copy()
    if active_cell:
      style.append(
        {
          "if": {"row_index": active_cell["row"]},
          "backgroundColor": "rgba(150, 180, 225, 0.2)",
          "border": "1px solid blue",
        },
      )
    return style
"""


if __name__ == '__main__':
    app.run(debug=True)

