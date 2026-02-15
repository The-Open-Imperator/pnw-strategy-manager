from dash import html, dcc

import plotly.graph_objects as go
"""
DESC: Creates a vertical bar with labels and matching percentages, uses flexbox
ARGS:
    elements list of dicts with the content {label, color, percentage}
RETURN:
    html.Div flexbox element
"""
def vertical_progress_bar(elements: list):
    boxes = list()

    for e in elements:
        boxStyle = {'width':f'{e["percentage"]}%', 'height':'20px', 'background-color':e["color"], 'text-align':'center'}
        boxes.append(html.Div(e['label'], style=boxStyle))
    return html.Div(html.Div(children=boxes, style={'display':'flex', 'flex-direction':'row'}), style= {'border-radius':'8px'})

"""

"""
def pichart(label: str, data: dict, colors: list):
    fig = go.Figure(data=[go.Pie(labels=list(data.keys()) , values=list(data.values()), hole=0.4)])
    fig.update_layout(
            showlegend=False, 
            margin={'b':0, 'l':0, 't':0, 'r':0},
            annotations=[dict(text=label, x=0.5, y=0.5,
                      font_size=20, showarrow=False, xanchor="center")])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    return dcc.Graph(figure=fig)

def pichart_member_colors(data: dict):
    dataCopy = dict()
    for key, value in data.items():
        if value > 0:
            dataCopy[key] = value

    fig = go.Figure(data=[go.Pie(title="Member colors",labels=list(dataCopy.keys()) , values=list(dataCopy.values()))])
    fig.update_layout(
            showlegend=False, 
            margin={'b':15, 'l':15, 't':15, 'r':15})
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=list(dataCopy.keys()), line=dict(color='#000000', width=2)))
    return dcc.Graph(figure=fig)


