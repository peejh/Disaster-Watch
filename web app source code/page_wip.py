import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State

from app import app
from app import db
from app import Tweet
import pbnj2


#-------------------------------------------------------------------------------------------------
# Layout

page_wip = dbc.Container(fluid=True, className='text-center py-4', style={'background-color':'rgb(28,22,22)'}, children=[
    dbc.Container(children=[
        html.Div(children=[
            html.Img(src='assets/wip.inthezone.gif', width='400px', className='img-fluid')
        ]),        
        html.H3("This page is under construction.", className="text-light mb-4"),
        html.P('We are sorry for the inconvenience. Try again later.', className='text-muted'),
        html.P(dbc.Button("Go to Dashboard", color="success", href='/'), className="mt-4"),
    ])
])

layout = page_wip


#-------------------------------------------------------------------------------------------------
# Callbacks