from dash import Dash, dash_table, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

from wartable import dash_wartable_format

from dataflow import init_wars_nations_from_allianceSet
from dataconvert import create_WarTable_from_wars_nations

allianceSet = {4221}
wars, nations = init_wars_nations_from_allianceSet(allianceSet)
warTable = create_WarTable_from_wars_nations(wars, nations)



app = Dash()

# Requires Dash 2.17.0 or later
app.layout = [
    html.H1(children='PnW Strategy Manager', style={'textAlign':'center'}),
    dash_wartable_format(warTable)
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

