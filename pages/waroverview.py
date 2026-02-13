import dash
from dash import Dash, dash_table, html, dcc, callback, Output, Input, State
import dash_cytoscape

from tables import dash_wartable_format
from cytograph import dash_cyto_format

from dataflow import init_wars_nations_from_allianceSet
from dataconvert import create_warTable_from_wars_nations, csv_str_to_set

dash.register_page(__name__,
                   path='/wars',
                   title='Overview wars',
                   name='Overview wars'
                  )


dataSettings = html.Center(
                    html.Fieldset(children = [
                        html.H3("Data Settings", style={'textAlign':'center', 'font-size':'34'}),
                        
                        html.Div("Get all wars from"),
                        dcc.Input(id='input_alliance_list', type='text', placeholder='AA list, ex: 4221, 1312'),
                        #dcc.Checklist(['Include applicants'], ['Include applicants'], id='include_applicants'),
                        html.Button("Apply & Pull data", id='btn_apply')
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
    html.H1(children='Overview Wars', style={'textAlign':'center'}),
    html.Div(html.Center(settings)),
    html.H1(children='War Table', style={'textAlign':'center'}),
    html.Div(id='wartable-div', children = [dash_table.DataTable(id='wartable')]),
    #html.H1(children='War Graph', style={'textAlign':'center'}),
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

