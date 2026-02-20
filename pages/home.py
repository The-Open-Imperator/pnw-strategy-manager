import dash
from dash import html, callback, Output, Input

from styles import *

from dataconvert import AllianceStats
from figures import vertical_progress_bar, pichart_war_type, pichart_member_colors, pichart_member_policies, pyramid_member_cities

dash.register_page(__name__, path='/')


leftBox = html.Fieldset(id="leftbox", children= [
            html.Center(html.H3("MA"))],
                        style= fieldSetFitFour
                       )

centerBox = html.Fieldset(id="centerbox", children = [
            html.Center(html.H3("Alliance"))],
                          style= fieldSetFitFour
                         )

rightBox = html.Fieldset(id="rightbox", children = [
            html.Center(html.H3("IA"))],
                         style= fieldSetFitFour
                        )

layout = html.Div([
    html.Div(id="dummy-div"),
    html.Center(html.H1('Home page')),
    html.Div(children= [
            leftBox,
            centerBox,
            rightBox
        ], style= flexBoxRowSpaced
            )
])

@callback(
    Output('leftbox', 'children'),
    Output('centerbox', 'children'),
    Output('rightbox', 'children'),
    Input('dummy-div', 'n_clicks')
)
def update_leftBox(nClicks):
    aaStats = AllianceStats({4221})

    pOff = int((aaStats.sumOffensiveWars / (aaStats.sumOffensiveWars + aaStats.sumDefensiveWars)) * 100)
    pDef = int((aaStats.sumDefensiveWars / (aaStats.sumOffensiveWars + aaStats.sumDefensiveWars)) * 100)
    barElements = [{'label':f'⚔️ {pOff}%', 'color':'aqua', 'percentage':pOff}, {'label':f'🛡️ {pDef}%', 'color':'crimson', 'percentage':pDef}]
    lb = [html.Center(html.H2("MA")),
          html.Center(html.Div(f'Offensive wars: {aaStats.sumOffensiveWars}')),
          html.Center(html.Div(f'Defensive wars: {aaStats.sumDefensiveWars}')),
          vertical_progress_bar(barElements),

          html.Center(html.Div("Offensive/Defensive war types:")),
          html.Div(children=[
              html.Div(pichart_war_type("⚔️", aaStats.sumOffensiveWarTypes, ['aqua', 'blue', 'darkblue']), style=fieldSetFitTwo), 
              html.Div(pichart_war_type("🛡️", aaStats.sumDefensiveWarTypes, ['crimson', 'red', 'darkred']), style=fieldSetFitTwo)
                            ] 
                   ,style=flexBoxRowCenter),

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
