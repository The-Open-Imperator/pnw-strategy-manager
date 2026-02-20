import dash
import dash_auth
from dash import Dash, html, dcc

VALID_USER_PASS_PAIR = {'Jewma':'test'}

app = Dash(__name__, use_pages=True)

auth = dash_auth.BasicAuth(app,
                           VALID_USER_PASS_PAIR,
                           secret_key="TEST")


app.layout = html.Div([
    html.Center(html.H1('PnW Strategy Manager', style={'textAlign':'center', 'font-size':'52'})),
    html.Center(html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ])),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)
