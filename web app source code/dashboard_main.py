import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State

import dash_table as dtable
from dash_table import FormatTemplate
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json

from app import app
from app import db
from app import Tweet
from app import Tweed
from app import Place
from app import Hashtag
import pbnj2

from sklearn.utils import shuffle   # DELETE LATER


#-------------------------------------------------------------------------------------------------
# Layout methods

def format_good_tweet_card(df, i):
    now = datetime.now() + timedelta(hours=4) # tweet timestamps are 4 hours ahead
    curr = df.at[i, 'last_tweeted_at']
    img_url = df.at[i,'user_profile_pic_url']
    user_name = df.at[i,'user_name']
    user_screen_name = '@' + df.at[i,'user_screen_name']
    user_verified = 'fas fa-check-circle mx-1 '
    user_verified += 'text-primary' if df.at[i, 'user_verified'] else 'text-muted'
    text = df.at[i, 'text']
    last_updated = pbnj2.get_pretty_timedelta(now - curr) 
    prob = int(round(df.at[i, 'prob_is_disaster'] * 100, 0))
    prob_str = str(prob) + '%'
    prob_class = pbnj2.get_prob_class(prob)
    replies = pbnj2.get_pretty_count(df.at[i, 'reply_count'])
    retweets = pbnj2.get_pretty_count(df.at[i, 'retweet_count'])
    favorites = pbnj2.get_pretty_count(df.at[i, 'favorite_count'])
    url_web = df.at[i, 'url_web_view']

    date_place_metadata = last_updated
    place_full_name = df.at[i, 'place_full_name']
    user_location = df.at[i, 'user_location']
    loc_name = place_full_name if place_full_name else user_location
    if loc_name:
        date_place_metadata += ' | ' + str(loc_name)

    return dbc.Card(className='p-0 ml-2 mb-2 shadow', children=[
        dbc.CardBody(className='p-2', children=[
            html.Div(className='row', children=[
                html.Div(className='col-auto', children=[
                    html.Img(src=img_url, width='40px', className='img-fluid', style={'border-radius':'50%'}),
                ]),
                html.Div(className='col', children=[
                    html.Div(className='row', children=[
                        html.Span(user_name, className="font-weight-bold"),
                        html.I(className=user_verified)                            
                    ]),
                    html.Div(className='row', children=[
                        html.Small(user_screen_name, className="text-muted"),
                    ]),
                ])
            ]),
            html.Div(className='row', children=[
                html.Div(className='col', children=[
                    html.Hr(className="my-1"),
                    html.P(text, className='mb-1', style={'line-height':'1','font-size':'small'}),
                    html.P(date_place_metadata, className='mb-2 font-italic text-muted', style={'line-height':'1','font-size':'small'}),
                    dbc.Progress(prob_str, value=prob, color=prob_class, style={'height':'13px'})
                ])
            ]),
        ]),
        dbc.CardFooter(className='pt-0 pb-1 px-1', children=[
            html.Div(className='row justify-content-around', children=[
                html.Div(className='col-auto', children=[
                    html.I(className='fas fa-comment text-muted mr-1'),
                    html.Small(replies, className='text-muted')
                ]),
                html.Div(className='col-auto', children=[
                    html.I(className='fas fa-retweet text-muted mr-1'),
                    html.Small(retweets, className='text-muted')
                ]),
                html.Div(className='col-auto', children=[
                    html.I(className='fas fa-heart text-muted mr-1'),
                    html.Small(favorites, className='text-muted')
                ]),
                html.Div(className='col-auto', children=[
                    html.A(href=url_web, children=[
                        html.I(className='fab fa-twitter', style=dict(color='#1DA1F2')),
                    ])
                ])
            ])
        ]),
    ])

#-------------------------------------------------------------------------------------------------
# Layout

tickers_bad = html.Div(
    className='bg-danger shadow text-light text-center px-2 py-2 mr-1',
    style={'border-radius':'4px'},
    children=[
        html.Label(className='h6 py-1', children=[
            html.I(className='fas fa-chart-line mr-2'),        
            'Off-located tweets',
        ]),
        html.Div(className='border-top pt-2', children=[
            html.Label('0', id='div-dashmain-tickers-bad', className='display-4')
        ]),
    ]
)

tickers_good = html.Div(
    className='bg-success shadow text-light text-center px-2 py-2 mr-1',
    style={'border-radius':'4px'},
    children=[
        html.Label(className='h6 py-1', children=[
            html.I(className='fas fa-chart-line mr-2'),        
            'On-topic tweets',
        ]),
        html.Div(className='border-top pt-2', children=[
            html.Label('0', id='div-dashmain-tickers-good', className='display-4')
        ]),
    ]
)

tickers_geoloc = html.Div(
    className='bg-info shadow text-light text-center px-2 py-2 mr-1',
    style={'border-radius':'4px'},
    children=[
        html.Label(className='h6 py-1', children=[
            html.I(className='fas fa-chart-line mr-2'),        
            'Geo-located tweets',
        ]),
        html.Div(className='border-top pt-2', children=[
            html.Label('0', id='div-dashmain-tickers-geoloc', className='display-4')
        ]),
    ]
)

tickers_userloc = html.Div(
    className='bg-primary shadow text-light text-center px-2 py-2',
    style={'border-radius':'4px'},
    children=[
        html.Label(className='h6 py-1', children=[
            html.I(className='fas fa-chart-line mr-2'),        
            'User-located tweets',
        ]),
        html.Div(className='border-top pt-2', children=[
            html.Label('0', id='div-dashmain-tickers-userloc', className='display-4')
        ]),
    ]
)

graph_dist_day = html.Div(
    className='bg-dark shadow text-light text-center p-1 mr-1',
    style={'border-radius':'4px'},
    children=[
        html.Label(className='h5 py-1', children=[
            html.I(className='fas fa-chart-bar mr-2'),        
            'Tweet distribution by date',
        ]),
        dcc.Graph(id='graph-dashmain-dist-day')
    ]
)

graph_dist_conf = html.Div(
    className='bg-dark shadow text-light text-center p-1',
    style={'border-radius':'4px'},
    children=[
        html.Label(className='h5 py-1', children=[
            html.I(className='fas fa-chart-bar mr-2'),        
            'Tweet distribution by confidence',
        ]),
        dcc.Graph(id='graph-dashmain-dist-conf')
    ]
)

graph_trending_hashtags = html.Div(
    className='bg-dark shadow text-light text-center p-1',
    # style={'border-radius':'4px'},
    children=[
        html.Label(className='h5 py-1', children=[
            html.I(className='fas fa-chart-bar mr-2'),        
            'Trending',
        ]),
        dcc.Graph(id='graph-dashmain-trend-hash')
    ]
)   

grid_layout = html.Div([
    dbc.Row(no_gutters=True, children=[
        dbc.Col(md=12, lg=9, children=[
            dbc.Row(no_gutters=True, className='my-3', children=[
                dbc.Col(width=12, children=[
                    html.Div(className='bg-dark p-1', children=[
                        dcc.Dropdown(id='drop-dashmain-location', className='mb-1',
                            clearable=True,
                            placeholder='Select a location...',
                            persistence=True,
                            persistence_type='session'
                        ),
                        html.Div(id='div-dashmain-map', className='shadow') 
                    ])
                ])
            ]),      
        ]),
        dbc.Col(md=12, lg=3, className='my-3', children=[
            graph_trending_hashtags
        ]),
    ]),
    dbc.Row(no_gutters=True, children=[
        dbc.Col([
            dbc.Row(no_gutters=True, className='my-3', children=[
                dbc.Col(sm=12, md=3, className='mb-2', children=[
                    tickers_bad
                ]),
                dbc.Col(sm=12, md=3, className='mb-2', children=[
                    tickers_good
                ]),
                dbc.Col(sm=12, md=3, className='mb-2', children=[
                    tickers_geoloc
                ]),
                dbc.Col(sm=12, md=3, className='mb-2', children=[
                    tickers_userloc
                ]),                
            ]),            
            dbc.Row(no_gutters=True, className='my-3', children=[
                dbc.Col(md=12, lg=6, className='mb-2', children=[
                    graph_dist_day
                ]),
                dbc.Col(md=12, lg=6, className='mb-2', children=[
                    graph_dist_conf
                ])             
            ])
        ])      
    ])
])

page_dashboard_main = dbc.Container(className='bg-secondary', fluid=True, children=[
    dcc.Interval(id='interval-dashmain-datatable', interval=1000*pbnj2.DASHMAIN_REFRESH_RATE, n_intervals=0),
    dcc.Interval(id='interval-dashmain-live', interval=1000*pbnj2.DASHMAIN_LIVE_RATE, n_intervals=0),
    dcc.Interval(id='interval-dashmain-drop-locations', interval=1000*pbnj2.DASHMAIN_REFRESH_RATE, n_intervals=0),
    # dashmain_map,
    grid_layout,
    html.Div(id='div-dashmain-secret-tweets', style={'display':'none'}),
    html.Div(id='div-dashmain-secret-locations', style={'display':'none'})
])

layout = page_dashboard_main

#-------------------------------------------------------------------------------------------------
# Callbacks

#~~~~~ Storing json data to secret div
@app.callback(
[
    Output('div-dashmain-secret-tweets', 'children'),
    Output('graph-dashmain-trend-hash', 'figure')
],    
[
    Input('interval-dashmain-datatable', 'n_intervals')
])
def retrieve_data(n_intervals):
    # custom_time = datetime(year=2021, month=4, day=1)
    timespan = datetime.now() + timedelta(hours=4) - timedelta(days=7)
    df = pd.read_sql(db.session.query(Tweet).filter(Tweet.last_tweeted_at >= timespan).order_by(Tweet.last_tweeted_at.desc()).statement, 
                        con=db.engine)
    df_hashtags = pd.read_sql(db.session.query(Hashtag).filter(Hashtag.recorded_at >= timespan).order_by(Hashtag.recorded_at.desc()).statement,
                        con=db.engine)
    
    #----- Calculate extra information
    df['engagement'] = pbnj2.extract_engagement_total(df)
    df['best_loc_lon'], df['best_loc_lat'] = pbnj2.extract_best_location(df)
    df['prob'] = df['prob_is_disaster'].apply(lambda x: int(round(x * 100, 0)))
    df['prob_class'] = df['prob'].apply(lambda x: pbnj2.get_prob_class(x))
    df['marker_color'] = df['prob_class'].apply(lambda x: pbnj2.DASHMAIN_MAP_MARKER_COLORS[x])
    df['tooltip_text'] = df.apply(lambda x: pbnj2.extract_tooltip_text(x), axis=1)

    #----- Draw trending hashtags graph
    # df2 = df[df.prob_is_disaster >= 0.8]
    # df_hashtags = df_hashtags[df_hashtags.tweet_id.isin(df2.id)]
    hashes = df_hashtags.groupby('word').word.count()
    hashes_t20 = hashes.sort_values().tail(20)
    hash_data = go.Bar(
                    x=hashes_t20.values,
                    y=hashes_t20.index,
                    orientation='h',
                    text=hashes_t20.index,
                    marker=dict(color='salmon'),
                    # marker_color=hashes_t20.values,
                    textposition='auto'
                )
    hash_layout = go.Layout(margin=dict(l=15, r=15, t=0, b=10, pad=2))
    fig_hash = go.Figure(hash_data, hash_layout)
    fig_hash.update_traces(hovertemplate='%{x}<extra></extra>')
    fig_hash.update_layout(
        height=618,
        plot_bgcolor='#343A40',
        paper_bgcolor='#343A40',
        font={'color':'#FBFBFB'},
        xaxis={'visible':False},
        yaxis={'visible':False},
    )

    return json.dumps(df.to_json(orient='split')), fig_hash

#~~~~~ Store locations data to secret div
@app.callback(
    Output('div-dashmain-secret-locations', 'children'),
[
    Input('interval-dashmain-drop-locations', 'n_intervals')
])
def retrieve_locations(n_intervals):
    df = pd.read_sql(db.session.query(Place).order_by(Place.country).statement, con=db.engine)
    return json.dumps(df.to_json(orient='split'))

#~~~~~ Update ticker counts and graphs
@app.callback(
[
    Output('div-dashmain-tickers-bad', 'children'),
    Output('div-dashmain-tickers-good', 'children'),
    Output('div-dashmain-tickers-geoloc', 'children'),
    Output('div-dashmain-tickers-userloc', 'children'),
    Output('graph-dashmain-dist-day', 'figure'),
    Output('graph-dashmain-dist-conf', 'figure')
],
[
    Input('interval-dashmain-live', 'n_intervals')
])
def update_live_components(n_intervals):
    timespan = datetime.now() + timedelta(hours=4) - timedelta(days=7)
    df_good = pd.read_sql(db.session.query(Tweet).filter(Tweet.last_tweeted_at >= timespan).statement, con=db.engine)   
    df_bad = pd.read_sql(db.session.query(Tweed).filter(Tweed.created_at >= timespan).statement, con=db.engine)

    #--------------------------------------------------
    good_count = df_good.shape[0]
    bad_count = df_bad.shape[0]
    geoloc_count = df_good.coordinates_lat.count()
    userloc_count = df_good.user_coords_lat.count()

    #--------------------------------------------------
    df_good['day'] = df_good['last_tweeted_at'].apply(lambda x: (x - timedelta(hours=4)).date())
    dates_good = df_good.groupby('day').day.count()
    trace_good = go.Bar(
                    x=dates_good.index.to_list(),
                    y=dates_good.values.tolist(),
                    name='On-topic',
                    marker={'color':'indianred'},
                    showlegend=True,
                    text=dates_good.values.tolist(),
                    textposition='auto'
                )
    df_bad['day'] = df_bad['created_at'].apply(lambda x: (x - timedelta(hours=4)).date())
    dates_bad = df_bad.groupby('day').day.count()
    trace_bad = go.Bar(
                    x=dates_bad.index.to_list(),
                    y=dates_bad.values.tolist(),
                    name='Off-topic',
                    marker={'color':'lightsalmon'},
                    showlegend=True,
                    text=dates_bad.values.tolist(),
                    textposition='auto'
                )
    day_data = [trace_good, trace_bad]
    day_layout = go.Layout(margin=dict(l=0, r=0, t=0, b=0, pad=2))
    fig_day = go.Figure(day_data, day_layout)
    fig_day.update_traces(hovertemplate='%{y}<extra></extra>')
    fig_day.update_layout(
        legend=dict(
            yanchor='top',
            y=0.99,
            xanchor='left',
            x=0.01
        ),
        plot_bgcolor='#343A40',
        paper_bgcolor='#343A40',
        font={'color':'#FBFBFB'}
    )

    #--------------------------------------------------
    df_good['prob'] = df_good['prob_is_disaster'].apply(lambda x: int(round(x * 100, 0)))
    df_good['prob_10s'] = df_good['prob'].apply(lambda x: str(x - (x % 10)) + 's')
    confs = df_good.groupby('prob_10s').prob_10s.count()
    colors = ['#6C757D','#F0AD4E','#5BC0DE','#5CB85C','#0275D8']
    trace_conf = go.Bar(
                    x=confs.index.to_list(),
                    y=confs.values.tolist(),
                    text=confs.values.tolist(),
                    textposition='auto',
                    marker_color=colors
                )
    conf_data = [trace_conf]
    conf_layout = go.Layout(margin=dict(l=0, r=0, t=0, b=0, pad=2))
    fig_conf = go.Figure(conf_data, conf_layout)
    fig_conf.update_traces(hovertemplate='%{y}<extra></extra>')
    fig_conf.update_layout(
        plot_bgcolor='#343A40',
        paper_bgcolor='#343A40',
        font={'color':'#FBFBFB'}
    )

    return bad_count, good_count, geoloc_count, userloc_count, fig_day, fig_conf

#~~~~~ Populate dropdown locations
@app.callback(
[
    Output('drop-dashmain-location', 'options'),
    Output('drop-dashmain-location', 'value')
],
[
    Input('div-dashmain-secret-locations', 'children')
])
def populate_locations(data):
    json_data = json.loads(data)
    df = pd.read_json(json_data, orient='split')
    df.sort_values(by='display_ascii', inplace=True)

    options = [dict(label=loc_name, value=str(id)) for id, loc_name in zip(df.nomin_id, df.display_ascii)]
    # default_nomin_id = str(pbnj2.DASHMAIN_MAP_DEFAULT_LOC)

    # return options, default_nomin_id
    return options, ''

#~~~~~ Populate the tweet sidebar
@app.callback(
    Output('div-dashmain-tweets-sidebar', 'children'),
[
    Input('div-dashmain-secret-tweets', 'children'),
    Input('drop-dashmain-location', 'value')
],
    State('div-dashmain-secret-locations', 'children')
)
def populate_tweet_cards(json_tweets, loc_id, json_locations):
    df_tweets = pd.read_json(json.loads(json_tweets), orient='split')
    df_locations = pd.read_json(json.loads(json_locations), orient='split')

    dff = df_tweets.loc[df_tweets.prob_is_disaster >= pbnj2.DASHMAIN_TWEETS_MIN_CONF]
    dff = dff[pd.notnull(dff.best_loc_lat)]

    if (loc_id):
        latitudes, longitudes = pbnj2.get_bbox(df_locations, int(loc_id))
        dff = dff[dff.apply(lambda x: pbnj2.is_within_boundingBox(x['best_loc_lat'], x['best_loc_lon'], latitudes, longitudes), axis=1)]

    dff = shuffle(dff) # DELETE LATER
    dff = dff.reset_index(drop=True)
    
    count = dff.shape[0]
    print(count)
    if count > 0:
        cardlist = []
        count = 4 if count > 4 else count
        for i in range(count):       
            cardlist.append(format_good_tweet_card(dff, i))

        return cardlist
    else:
        return html.H4('There are currently no tweets from this area', className='text-light')

#~~~~~ Updating the map
@app.callback(
    Output('div-dashmain-map', 'children'),
[
    Input('div-dashmain-secret-tweets', 'children'),
    Input('drop-dashmain-location', 'value')
],
    State('div-dashmain-secret-locations', 'children')
)
def update_map(json_tweets, loc_id, json_locations):
    # retrieve tweet locations
    df_tweets = pd.read_json(json.loads(json_tweets), orient='split')
    df_tweets_filtered = df_tweets.loc[~(np.isnan(df_tweets['best_loc_lon']))]
    lat = pbnj2.DASHMAIN_MAP_DEFAULT_LAT
    lon = pbnj2.DASHMAIN_MAP_DEFAULT_LON
    zoom = pbnj2.DASHMAIN_MAP_DEFAULT_ZOOM

    if (loc_id):
        # retrieve map location data
        df_locations = pd.read_json(json.loads(json_locations), orient='split')
        lat = float(df_locations.loc[df_locations.nomin_id == int(loc_id),'lat'])
        lon = float(df_locations.loc[df_locations.nomin_id == int(loc_id),'lon'])
        zoom = float(df_locations.loc[df_locations.nomin_id == int(loc_id),'zoom'])

    fig = go.Figure(go.Scattermapbox(
        lat=df_tweets_filtered['best_loc_lat'],
        lon=df_tweets_filtered['best_loc_lon'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            color=df_tweets_filtered['marker_color'],
            size=8,
            opacity=0.67
        ),
    ))

    fig.update_traces(hovertemplate=df_tweets_filtered['tooltip_text'])

    fig.update_layout(
        height=620,
        # autosize=True,
        hovermode='closest',
        mapbox=dict(
            style='open-street-map',
            center=go.layout.mapbox.Center(
                lat=lat,
                lon=lon
            ),
            pitch=0,
            zoom=zoom
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
    )

    return dcc.Graph(
        id='dashmain-map',
        figure=fig
    )
