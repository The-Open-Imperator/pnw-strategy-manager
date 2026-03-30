import dash
from dash import Dash, html, dcc

# DESC: Defines the navigation bar rendered on top of the pages.

def navbar_div():
    return html.Div([
        html.Center(html.Img(src='assets/SAM-Text.svg')),
        html.Center(html.Div([
            html.Div(
                dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
                ) for page in dash.page_registry.values()
                             ]))
        ])
