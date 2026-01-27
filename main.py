from dash import Dash, dash_table, html, dcc, callback, Output, Input, State
import dash_cytoscape
import pandas as pd

from wartable import dash_wartable_format
from cytograph import dash_cyto_format

from dataflow import init_wars_nations_from_allianceSet
from dataconvert import create_warTable_from_wars_nations, csv_str_to_set


dataSettings = html.Center(
                    html.Fieldset(children = [
                        html.H3("Data Settings", style={'textAlign':'center', 'font-size':'34'}),
                        dcc.Input(id='input_alliance_list', type='text', placeholder='AA list, ex: 4221, 1312'),
                        dcc.Input(id='input_sphere_list', type='text', placeholder='AA list, ex: 1, 2, 3, 4'),
                        dcc.Checklist(['Include Applicants'], ['Include Applicants']),
                        html.Button("Apply & Pull data", id='btn_apply')
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
    html.Div(id='wartable', children = []),
    html.Div(id='wargraph', children = [])
    ]


@callback(
    Output('wartable', 'children'),
    Output('wargraph', 'children'),
    Input('btn_apply', 'n_clicks'),
    State('input_alliance_list', 'value'),
    State('input_sphere_list', 'value'),
    prevent_initial_call=True
)
def update_data(n_clicks, allianceList, sphereList):
    wars, nations = init_wars_nations_from_allianceSet(csv_str_to_set(allianceList))
    warTable = create_warTable_from_wars_nations(wars, nations)
    return ([dash_wartable_format(warTable)], [dash_cyto_format(wars, nations)])

if __name__ == '__main__':
    app.run(debug=True)

