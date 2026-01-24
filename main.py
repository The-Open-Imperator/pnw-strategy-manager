from dash import Dash, dash_table, html, dcc, callback, Output, Input
import dash_cytoscape as cyto
import pandas as pd

from wartable import dash_wartable_format
from cytograph import dash_cyto_format

from dataflow import init_wars_nations_from_allianceSet
from dataconvert import create_WarTable_from_wars_nations

#allianceSet = {4221, 3339, 12480, 11009, 1210, 7484, 13295}
#allianceSet = {4221, 7484}
allianceSet = {4221}
wars, nations = init_wars_nations_from_allianceSet(allianceSet)
warTable = create_WarTable_from_wars_nations(wars, nations)



app = Dash()

# Requires Dash 2.17.0 or later
app.layout = [
    html.H1(children='PnW Strategy Manager', style={'textAlign':'center'}),
    html.Div(children = [dash_wartable_format(warTable)]),
    html.Div(children = [dash_cyto_format(wars, nations)])
    ]

"""
@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')
"""
if __name__ == '__main__':
    app.run(debug=True)

