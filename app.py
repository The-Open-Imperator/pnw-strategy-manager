import dash
import dash_auth
from dash import Dash, html, dcc

VALID_USER_PASS_PAIR = {'Jewma':'test'}

app = Dash(__name__, use_pages=True)

auth = dash_auth.BasicAuth(app,
                           VALID_USER_PASS_PAIR,
                           secret_key="ASD3dd0a0j9sda#s",
                           public_routes=["/", "/assets/Speedy.ttf", "/assets/styles.css", "/assets/SAM-Logo-Text.svg"])


if __name__ == '__main__':
    app.run(debug=True)
