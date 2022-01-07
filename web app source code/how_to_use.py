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

page_about_us = html.Div(className='container py-4', children=[
    html.H1('How to Use'),
    html.P(pbnj2.LOREM_IPSUM),
])

layout = page_about_us


#-------------------------------------------------------------------------------------------------
# Callbacks