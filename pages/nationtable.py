import dash
from dash import Dash, dash_table, html, dcc, callback, Output, Input, State

import logging
logger = logging.getLogger("MAINLOG")

import userhandler
from errorstates import UserProfileLoadSTATUS, GameApiReturnSTATUS

from tables import dash_nationtable_format

from dataflow import NationsFromAAIDSet
from dataconvert import csv_str_to_set

from utils import DEFAULT_NATION_FILTER
from .nav_bar import navbar_div

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
                        html.H3("DATA Settings"),
                        html.Div("Get all nations from"),
                        dcc.Input(id='input_enemy_list', type='text', placeholder='AA list, ex: 4221, 1312'),
                        nationFilterChecklist,
                        html.Button("APPLY", id='btn_apply_enemy', className="btn-search")
                                             ],
                                )
                          )

settings = html.Fieldset(children = [
                            html.H2("Settings"),
                            dataSettings
                                    ],
                                    className="field-medium"
                        )

def layout(**kwargs):
    logger.info("User %s accessed the nations page.", userhandler.get_username())
    return [
    navbar_div(),
    html.Center(html.H1(children='Nation Table')),
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

    logger.info("Nation Search for %s, IDs=(%s), FILTER=(%s)", userhandler.get_username(), allianceList, excludeFilter)
    
    allianceSet = csv_str_to_set(allianceList)
    nationDat = NationsFromAAIDSet(allianceSet, excludeFilter)
    if (nationDat.status.value):
        logger.error(f"[ERR_{nationDat.status}] in Nation Search for %s, IDs=(%s), FILTER=(%s)", userhandler.get_username(), allianceList, excludeFilter)
        return [html.Center(html.Div(f"[ERR_{nationDat.status}]"))]

    return [dash_nationtable_format(nationDat.nations)]
