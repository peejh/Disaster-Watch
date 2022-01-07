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

page_not_found = dbc.Container(fluid=True, className='text-center py-4', style={'background-color':'#152744'}, children=[
    dbc.Container(children=[
        html.Div(className='mb-5', children=[
            html.Img(src='assets/404.earthrotation.gif', className='img-fluid')
        ]),        
        html.H3("This page does not exist.", className="text-light mb-4"),
        html.P('We are sorry for the inconvenience. Please circle back.', className='text-muted'),
        html.P(dbc.Button("Go to Dashboard", color="success", href='/'), className="mt-4"),
    ])
])

layout = page_not_found


#-------------------------------------------------------------------------------------------------
# Callbacks