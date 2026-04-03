import dash
from dash import html, callback, Output, Input

import logging
logger = logging.getLogger("MAINLOG")

import userhandler

from .nav_bar import navbar_div

from dataconvert import AllianceStats
from figures import vertical_progress_bar, pichart_war_type, pichart_member_colors, pichart_member_policies, pyramid_member_cities

dash.register_page(__name__, path='/home')
# PAGE: home
# PATH: /home
# ACCESS: AUTHENTICATED
# DESC: Statistics dashboard for the users alliance.


leftBox = html.Fieldset(id="leftbox", children= [html.Center(html.H3("MA"))],
                            className= "field-fit-four"
                       )

centerBox = html.Fieldset(id="centerbox", children = [html.Center(html.H3("Alliance"))],
                            className= "field-fit-four"
                         )

rightBox = html.Fieldset(id="rightbox", children = [html.Center(html.H3("IA"))],
                            className= "field-fit-four" 
                        )

def layout(**kwargs):
    user = userhandler.UserData()
    if user.status.value:
        return html.Div(f"[ERR_{user.status}] Something went wrong when loading the user profile.")
    return html.Div([
    navbar_div(),
    html.Div(id="dummy-div"),
    html.Center(html.H1(user.title + " " + user.username)),
    html.Div(children= [
            leftBox,
            centerBox,
            rightBox
        ], className= "flexbox-row-space"
            )
])

@callback(
    Output('leftbox', 'children'),
    Output('centerbox', 'children'),
    Output('rightbox', 'children'),
    Input('dummy-div', 'n_clicks')
)
def update_leftBox(nClicks):
    user = userhandler.UserData()
    if user.status.value:
        errDiv = html.Div(f"[ERR_{user.status}] Userprofile Error!")
        return [errDiv, errDiv, errDiv]
    logger.info("User %s accessed home.", user.username)

    aaStats = AllianceStats({user.allianceid})

    pOff = int((aaStats.sumOffensiveWars / (aaStats.sumOffensiveWars + aaStats.sumDefensiveWars)) * 100)
    pDef = int((aaStats.sumDefensiveWars / (aaStats.sumOffensiveWars + aaStats.sumDefensiveWars)) * 100)
    barElements = [{'label':f'⚔️ {pOff}%', 'color':'aqua', 'percentage':pOff}, {'label':f'🛡️ {pDef}%', 'color':'crimson', 'percentage':pDef}]
    lb = [html.Center(html.H2("MA")),
          html.Center(html.Div(f'Offensive wars: {aaStats.sumOffensiveWars}')),
          html.Center(html.Div(f'Defensive wars: {aaStats.sumDefensiveWars}')),
          vertical_progress_bar(barElements),

          html.Center(html.Div("Offensive/Defensive war types:")),
          html.Div(children=[
              html.Div(pichart_war_type("⚔️", aaStats.sumOffensiveWarTypes, ['aqua', 'blue', 'darkblue']), className= "field-fit-two"), 
              html.Div(pichart_war_type("🛡️", aaStats.sumDefensiveWarTypes, ['crimson', 'red', 'darkred']), className= "field-fit-two")
                            ], className= "flexbox-row-center"
                  ),

          html.Center(html.Div("War policies:")),
          html.Center(html.Div(pichart_member_policies(aaStats.sumWarPolicies)))
        ]

    cb = [html.Center(html.H1(aaStats.name)),
          html.Center(html.Img(src=aaStats.flag, style={'height':'250px', 'width':'auto'})),
          html.Center(html.Div(f'Score: {aaStats.score}')),
          html.Center(html.Div(f'Rank: #{aaStats.rank}')),
          html.Center(html.Div(f'Members: {aaStats.sumMembers}')),
          html.Center(html.Div(f'Color: {aaStats.color}')),

          html.Center(html.Div("City distribution:")),
          html.Center(html.Div(pyramid_member_cities(aaStats.cityDistribution)))
         ]

    rb = [html.Center(html.H2("IA")),
          html.Center(html.Div(f'Cities: {aaStats.sumCities}')),
          html.Center(html.Div('Member colors:')),
          html.Center(html.Div(pichart_member_colors(aaStats.sumColors))),
          html.Center(html.Div('Domestic policies:')),
          html.Center(html.Div(pichart_member_policies(aaStats.sumDomesticPolicies)))
         ]

    return [lb, cb, rb]
