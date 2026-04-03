import dash
from dash import Dash, dash_table, html, dcc, callback, Output, Input, State
import dash_cytoscape

import logging
logger = logging.getLogger("MAINLOG")

import userhandler
from errorstates import UserProfileLoadSTATUS, GameApiReturnSTATUS

from .nav_bar import navbar_div

from tables import dash_wartable_format
from cytograph import dash_cyto_format

from dataflow import WarsNationsFromAAIDSet
from dataconvert import create_warTable_from_wars_nations, csv_str_to_set

dash.register_page(__name__, path='/wars', title='Overview wars', name='Overview wars')
# PAGE: wars
# PATH: /wars
# DESC: Provides an overview of all active wars as a table and graph view.


dataSettings = html.Center(
                    html.Fieldset(children = [
                        html.H3("DATA Settings"), 
                        html.Div("Get all wars from"),
                        dcc.Input(id='input_alliance_list', type='text', placeholder='AA list, ex: 4221, 1312'),
                        html.Button("APPLY", id='btn_apply', className="btn-search")
                                             ]
                                )
                          )

settings = html.Fieldset(children = [
                            html.H2("Settings"),
                            dataSettings
                                    ],
                                    className="field-medium"
                        )

def layout(**kwargs):
    logger.info("User %s accessed the wars page.", userhandler.get_username())
    return [
    navbar_div(),
    html.Center(html.H1(children='Overview Wars')),
    html.Div(html.Center(settings)),
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
    logger.info("Wars overview for %s, IDs=(%s)", userhandler.get_username(), allianceList)

    wnDat = WarsNationsFromAAIDSet(csv_str_to_set(allianceList))
    if (wnDat.status.value):
        logger.error("[ERR_{%s}] in Wars overview for %s, IDs=(%s)", wnDat.status ,userhandler.get_username(), allianceList)
        errDiv = html.Center(html.Div(f"[ERR_{wnDat.status}]"))
        return [errDiv, errDiv]

    warTable = create_warTable_from_wars_nations(wnDat.wars, wnDat.nations)
    return [dash_wartable_format(warTable), dash_cyto_format(wnDat.wars, wnDat.nations)]

