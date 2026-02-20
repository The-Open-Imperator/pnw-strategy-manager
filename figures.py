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
def pichart_war_type(label: str, data: dict, colors: list):
    fig = go.Figure(data=[go.Pie(labels=list(data.keys()) , values=list(data.values()), hole=0.4)])
    fig.update_layout(
            height=200,
            showlegend=False, 
            margin={'b':1, 'l':1, 't':1, 'r':1},
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

    fig = go.Figure(data=[go.Pie(labels=list(dataCopy.keys()) , values=list(dataCopy.values()))])
    fig.update_layout(
            height=250,
            width=250,
            showlegend=False, 
            margin={'b':1, 'l':1, 't':1, 'r':1})
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=list(dataCopy.keys()), line=dict(color='#000000', width=2)))
    return dcc.Graph(figure=fig)

def pichart_member_policies(data: dict):
    dataCopy = dict()
    for key, value in data.items():
        if value > 0:
            dataCopy[key] = value

    fig = go.Figure(data=[go.Pie(labels=list(dataCopy.keys()) , values=list(dataCopy.values()))])
    fig.update_layout( 
            height=500,
            width=400,
            margin={'b':1, 'l':1, 't':1, 'r':1},
            legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="right",
                    x=0.95))
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=list(dataCopy.keys()), line=dict(color='#000000', width=2)))
    return dcc.Graph(figure=fig)

def pyramid_member_cities(data: dict):
    dataCopy = dict()
    for key,value in data.items():
        dataCopy[key] = -value

    fig = go.Figure()
    fig.add_trace(go.Bar(y=list(data.keys()),
                         x=list(data.values()),
                         name='Cities',
                         orientation='h',
                         marker_color='red'
                        )
                 )
    fig.add_trace(go.Bar(y=list(dataCopy.keys()),
                         x=list(dataCopy.values()),
                         name='Cities',
                         orientation='h',
                         marker_color='red'
                        )
                 )
    
    fig.update_yaxes(
            anchor="free",
            position=0.05
                    )
    fig.update_layout(
            height=450,
            width=400,
            margin={'b':1, 'l':1, 't':1, 'r':1},
            showlegend=False,
            barmode='relative',
            bargap = 0.0,
            bargroupgap = 0,
            barcornerradius=5
                     )
    return dcc.Graph(figure=fig)
