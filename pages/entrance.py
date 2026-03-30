import dash
from dash import html

import logging 
logger = logging.getLogger("MAINLOG")

import userhandler

from styles import loginButton

dash.register_page(__name__, path='/')
# PAGE: entrance
# PATH: /
# ACCESS: UNAUTHENTICATED
# DESC: Initial landing page that is used to refer to the Basic Auth, can be skipped by directly accessing protected pages.

def layout(**kwargs):
    logger.info("User %s accessed the entrance.", userhandler.get_username())
    return html.Div([
        html.Center(html.Img(src='assets/SAM-Logo-Text.svg')),
        html.Center(html.A("ESTABLISH UPLINK", href='./home', style=loginButton))
    ])
