import dash
import dash_auth
from dash import Dash, html, dcc

import logging
logger = logging.getLogger("MAINLOG")

## LOGGING SETUP CONSOLE + FILE
logger.setLevel("INFO")

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("./SAM.log", mode="a", encoding="utf-8")
logger.addHandler(console_handler)
logger.addHandler(file_handler)

form = logging.Formatter(
        "{asctime} - {levelname} - {message}",
        style = "{",
        datefmt = "%Y-%m-%d %H:%M:%S"                        )
console_handler.setFormatter(form)
file_handler.setFormatter(form)


VALID_USER_PASS_PAIR = {'Jewma':'test', 'Toxic':'tset'}

# With page validation
#app = Dash(__name__, use_pages=True)
# Without page validation
app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)

app._favicon = ("/assets/favicon.ico")

auth = dash_auth.BasicAuth(app,
                           VALID_USER_PASS_PAIR,
                           secret_key="ASD3dd0a0j9sda#s",
                           public_routes=["/", "/assets/Speedy.ttf", "/assets/styles.css", "/assets/SAM-Logo-Text.svg", "/assets/favicon.ico"])

logger.info("Successfully initialized SAM web.")

#if __name__ == '__main__':
#    logger.info("Startup DONE, ready to serve Spectre.")
#    app.run() #(debug=True)
