# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State

from app import app
import dashboard_main
import livefeed
import how_to_use
import about_us
import help_hotlines
import feedback
import disclaimer
import page_404
import page_wip
import pbnj2


#-------------------------------------------------------------------------------------------------
# Layout

categories = ['Accident', 'Storm', 'Typhoon', 'Earthquake', 'Eruption', 'Landslide', 'Hurricane']

nav4 = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col([
                        html.Div(className='bg-danger border', style={'border-radius':'5px'}, children=[
                            html.I(className='fas fa-bullhorn text-light mx-2')
                        ])
                    ]),
                    dbc.Col(dbc.NavbarBrand(html.H2(pbnj2.BRAND_NAME, className='text-light mx-2 mb-0', style={'font-family':'Monoton'}))),
                ],
                align="center",
                no_gutters=True,
            ),
            href="/",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(
            [
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink('Dashboard', active='exact', href='/', className='m-1')),
                        dbc.NavItem(dbc.NavLink('Live Feed', active='exact', href='/livefeed', className='m-1')),
                    ],
                    navbar=True,
                    pills=True,
                )
            ],
            id="navbar-collapse",
            navbar=True
        ),
    ],
    fixed='top',
    sticky='top',
    color='dark',
    dark=True,
)

footer = html.Footer(className='footer bg-danger px-5', children=[
    html.Div(className='container', children=[
        html.Div(className='row justify-content-center pt-4', children=[
            html.Img(src='assets/lassondeLogo2.png', width='200px', className='img-fluid')
        ]),
        html.Div(className='row pt-3', children=[
            html.Div(className='col text-center', children=[
                html.Ul(className='breadcrumb bg-danger justify-content-center', children=[
                    html.Li(dcc.Link('How to Use', href='/how-to-use', className='text-light'), className='breadcrumb-item'),
                    html.Li(dcc.Link('About Us', href='/about-us', className='text-light'), className='breadcrumb-item'),
                    html.Li(dcc.Link('Help hotlines', href='/help-hotlines', className='text-light'), className='breadcrumb-item'),                    
                    html.Li(dcc.Link('Feedback', href='/feedback', className='text-light'), className='breadcrumb-item'),
                    html.Li(dcc.Link('Disclaimer', href='/disclaimer', className='text-light'), className='breadcrumb-item'),
                ], style={'border':'none'})
            ])
        ]),
        html.Div(className='row border-top pt-3', children=[
            html.Div(className='col text-center text-light small', children=[
                html.P('Copyright © 2021 ' + pbnj2.BRAND_NAME + '. All rights reserved.')
            ])
        ])
    ])
])

# Main APP LAYOUT
app.layout = html.Div(id='page', children=[
    dcc.Location(id='url', refresh=False),
    nav4,
    html.Div(id='page-content'),
    footer
])


#-------------------------------------------------------------------------------------------------
# Callbacks

# Toggler for navbar-collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return 

# Switching pages
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return dashboard_main.layout
    elif pathname == '/livefeed':
        return livefeed.layout
    elif pathname == '/about-us':
        return page_wip.layout
    elif pathname == '/how-to-use':
        return page_wip.layout
    elif pathname == '/help-hotlines':
        return help_hotlines.layout        
    elif pathname == '/feedback':
        return page_wip.layout
    elif pathname == '/disclaimer':
        return page_wip.layout
    else:
        return page_404.layout


#-------------------------------------------------------------------------------------------------
# Main

if __name__ == '__main__':
    app.run_server(debug=True)