import dash
from dash import Dash, dash_table, html, dcc, callback, Output, Input, State

from tables import dash_nationtable_format

from dataflow import init_nations_from_allianceSet
from dataconvert import csv_str_to_set

from utils import DEFAULT_NATION_FILTER

dash.register_page(__name__, 
                   path='/nations',
                   title='Nation Table',
                   name='Nation Table'
                  )

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
                        
                        html.Div("Get all nations from"),
                        dcc.Input(id='input_enemy_list', type='text', placeholder='AA list, ex: 4221, 1312'),
                        nationFilterChecklist,
                        html.Button("Apply & Pull data", id='btn_apply_enemy')
                                             ],
                                  style = {'width':'400px', 'border-radius':'8px'}
                                )
                          )

settings = html.Fieldset(children = [
                            html.H2("Settings", style={'textAlign':'center', 'font-size':'38'}),
                            dataSettings
                                    ],
                                    style = {'width':'820px', 'border-radius':'16px'}
                        )

layout = [
    html.H1(children='Nation Table', style={'textAlign':'center', 'font-size':'42'}),
    html.Div(html.Center(settings)),
    html.Div(id='enemytable-div', children = []),
    ]


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
    
    return [dash_nationtable_format(nations)]
