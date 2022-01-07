import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import callback_context
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json

from app import app
from app import db
from app import Tweet
from app import Tweed
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
    if loc_name and str(loc_name).lower() != 'nan':
        date_place_metadata += ' | ' + str(loc_name)

    return dbc.Card(className='p-0 mb-2 shadow', children=[
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

def format_bad_tweet_card(df, i):
    now = datetime.now() + timedelta(hours=4) # tweet timestamps are 4 hours ahead
    curr = df.at[i, 'created_at']
    text = df.at[i, 'text']
    last_updated = pbnj2.get_pretty_timedelta(now - curr) 
    prob = int(round(df.at[i, 'prob_is_disaster'] * 100, 0))
    prob_str = str(prob) + '%'
    prob_class = pbnj2.get_prob_class(prob)
    url_web = df.at[i, 'url_web_view']

    return dbc.Card(className='p-0 mb-2 shadow', color=prob_class, inverse=True, children=[
        dbc.CardBody(className='p-2', children=[
            html.Div(className='row', children=[
                html.Div(className='col', children=[
                    html.P(text, className='mb-1', style={'line-height':'1','font-size':'small'}),
                    html.P(last_updated, className='mb-2 font-italic', style={'line-height':'1','font-size':'small'}),
                ])
            ]),
        ]),
        dbc.CardFooter(className='pt-0 pb-1 px-1', children=[
            html.Div(className='row justify-content-around', children=[
                html.Div(className='col-auto', children=[
                    html.Small(prob_str, className='text-light font-weight-bold')
                ]),
                html.Div(className='col-auto'),
                html.Div(className='col-auto'),                
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

conf_slider = dcc.RangeSlider(id='slider-livefeed-confidence', min=0, max=100, step=5, pushable=1, allowCross=False,
                              value=[0,100], marks={val:(str(val) if val % 20 == 0 else '') for val in range(0,101,10)})

timeframe_items = ['Last minute', 'Last 5 minutes', 'Last 30 minutes', 'Last hour', 'Last 6 hours', 'Last 12 hours',
                   'Last day', 'Last 3 days', 'Last 7 days']
timeframe_select = dbc.Select(id='select-livefeed-timeframe', options=[
    dict(label=choice, value=i) for choice, i in zip(timeframe_items, range(len(timeframe_items)))
], value='8')

verified_opt = dbc.RadioItems(id='radio-livefeed-verified',
    options=[
        {'label': 'Yes', 'value': 'True'},
        {'label': 'No', 'value': 'False'},
    ],
    value='False',
    labelStyle={'display': 'inline-block'},
    className='text-light mx-3',
    labelClassName='mr-4',
    inputClassName='mr-2'
)

engagement_input = dbc.Input(id='input-livefeed-engagement',
    type='number',
    placeholder='0',
    value='0',
)

filters_sidebar = html.Div(className='bg-dark px-3 py-4 shadow mb-4', style={'border-radius':'4px'}, children=[
    dbc.FormGroup([
        dbc.Label('Confidence', html_for='slider-livefeed-confidence', className='text-light mx-3'),
        conf_slider,
    ]),
    dbc.Form([      
        dbc.FormGroup([
            dbc.Label('Time frame', html_for='select-livefeed-timeframe', className='text-light', width=5),
            dbc.Col(timeframe_select, width=7)
        ], row=True),   
        dbc.FormGroup([
            dbc.Label('Engagement', html_for='input-livefeed-engagement', className='text-light', width=5),
            dbc.Col(engagement_input, width=7)
        ], row=True),
        dbc.FormGroup([
            dbc.Label('Verified only', html_for='radio-livefeed-verified', className='text-light', width=5),
            dbc.Col(verified_opt, width=7)
        ], row=True), 
    ], className='px-3'),
    dbc.Button('Apply', id='button-livefeed-applyfilter', color='primary', block=True, outline=True, className='mt-5', style={'border-radius':'15px'})
])

search_layout = dbc.Container(className='mb-4', children=[
    html.Div(className='box shadow mb-2', children=[
        html.I(className='fa fa-search'),        
        dbc.Input(type='search', id='input-livefeed-search-keyword', placeholder='Search for disasters...'),
    ]),
    html.Div(className='mb-2', children=[
        dbc.Row(className='align-items-end border-bottom py-2 text-beige', children=[
            dbc.Col(sm=12, md=6, className='text-sm-center text-md-left', children=[
                html.H3(id='label-livefeed-results-count'),
            ]),
            dbc.Col(sm=12, md=6, className='text-sm-center text-md-right', children=[
                html.Span('Timestamp', className='h5 mr-1'),
                html.I(className='fas fa-sort mr-3 text-dgrey'),
                html.Span('Confidence', className='h5 mr-1'),
                html.I(className='fas fa-sort text-dgrey'),
            ])
        ])
    ]),
    html.Div(id='div-livefeed-search-filter', className='mb-4', style={'display':'none'}, children=[
        dbc.Badge(id='badge-livefeed-search-filter', href='#', pill=True, color='warning', className='py-1 px-2', children=[
            html.Span(id='label-livefeed-search-keyword'),
            html.I(className='fas fa-times ml-1')
        ])
    ])
])

loadmore_button = html.Div(id='div-livefeed-loadmore-button', className='text-center', style={'display':'none'}, children=[
    dbc.Button(
        'Load more...',
        id='button-livefeed-loadmore', 
        color='warning', 
        outline=True, 
        className='text-center mt-2',
        style={'border-radius':'15px'}
    )
])

noresults_layout = dbc.Container(className='text-center py-4', style={'height':'520px'}, children=[
    html.Div(className='my-5', children=[
        html.Img(src='assets/noresults.png', className='img-fluid') 
    ]),  
])

page_livefeed = dbc.Container(className='bg-secondary py-3', fluid=True, children=[
    dcc.Interval(id='interval-livefeed', interval=1000*pbnj2.LIVEFEED_REFRESH_RATE, n_intervals=0),
    dbc.Row(children=[
        dbc.Col(md=12, lg=3, children=[
            filters_sidebar,
        ]),
        dbc.Col(md=12, lg=9, children=[
            search_layout,
            html.Div(id='div-livefeed-tweets', children=[]),
            loadmore_button,
            html.Label('0', id='label-livefeed-loadmore-page', hidden=True)
        ])
    ]),
    html.Div(id='div-livefeed-secret-main', style={'display':'none'}),
    html.Div(id='div-livefeed-secret-filter', style={'display':'none'}),
    html.Div(id='div-livefeed-secret-search', style={'display':'none'}),
])

layout = page_livefeed

#-------------------------------------------------------------------------------------------------
# Callbacks

#~~~~~ Storing json data to secret div
@app.callback(
    Output('div-livefeed-secret-main', 'children'),
    Input('interval-livefeed', 'n_intervals'),
)
def retrieve_data(n_intervals):
    timespan = datetime.now() + timedelta(hours=4) - timedelta(days=7)
    df_good = pd.read_sql(db.session.query(Tweet).filter(Tweet.last_tweeted_at >= timespan).order_by(Tweet.last_tweeted_at.desc()).statement, con=db.engine)
    df_bad = pd.read_sql(db.session.query(Tweed).filter(Tweed.created_at >= timespan).order_by(Tweed.created_at.desc()).statement, con=db.engine)
    
    df_good['engagement'] = pbnj2.extract_engagement_total(df_good)              
    df_bad['last_tweeted_at'] = df_bad['created_at']
    df_bad['engagement'] = 0
    df = pd.concat([df_good, df_bad], axis=0, ignore_index=True)
    df = df.sort_values(by='last_tweeted_at', ascending=False)

    return json.dumps(df.to_json(orient='split'))

#~~~~~ Applying filter and storing to secret intermediate div
@app.callback(
    Output('div-livefeed-secret-filter', 'children'),
[
    Input('button-livefeed-applyfilter', 'n_clicks'),
    State('div-livefeed-secret-main', 'children'),
    State('slider-livefeed-confidence', 'value'),
    State('select-livefeed-timeframe', 'value'),
    State('radio-livefeed-verified', 'value'),
    State('input-livefeed-engagement', 'value')           
])
def filter_data(btn_filter_nclicks, div_main_data, sld_conf_value, sel_time_value, rdi_verf_value, inp_eng_value):
    if btn_filter_nclicks:
        json_data = json.loads(div_main_data)
        df = pd.read_json(json_data, orient='split')

        # by confidence
        min_val = sld_conf_value[0]
        max_val = sld_conf_value[1]
        df = df.loc[(df['prob_is_disaster'] >= min_val / 100) & (df['prob_is_disaster'] <= max_val / 100)]

        # by time frame
        minutes, hours, days = pbnj2.get_timeframe(int(sel_time_value))
        timespan = datetime.now() + timedelta(hours=4) - timedelta(days=days, hours=hours, minutes=minutes)
        df = df.loc[df['last_tweeted_at'] >= timespan]

        # by verified status
        verf_val = rdi_verf_value == 'True'
        if verf_val:
            df = df.loc[df['user_verified'] == verf_val]

        # by engagement
        eng_val = int(inp_eng_value)
        df = df.loc[df['engagement'] >= eng_val]

        return json.dumps(df.to_json(orient='split'))
    else:
        raise PreventUpdate

#~~~~~ Applying keyword
@app.callback(
    Output('div-livefeed-secret-search', 'children'),
[
    Input('div-livefeed-secret-main', 'children'),    
    Input('div-livefeed-secret-filter', 'children'),           
    Input('input-livefeed-search-keyword', 'value'),
])
def search_data(main_data, filter_data, keyword):
    ctx = callback_context
    if ctx.triggered:
        ctx_id = ctx.triggered[0]["prop_id"].split(".")[0]
        print('ctx_id=' + ctx_id + ' in apply keyword callback...')
        print(type(keyword))
        print(str(keyword))   
        if str(keyword) != '':
            data = filter_data if filter_data else main_data
            df = pd.read_json(json.loads(data), orient='split')
            
            if df.shape[0] > 0:
                wordlist = str(keyword).split()
                for word in wordlist:
                    df = df.loc[df.text.str.contains(word, case=False)]
            
            return json.dumps(df.to_json(orient='split'))
        else:
            print('empty keyword in search_data is invoked...')            
            if ctx_id == 'input-livefeed-search-keyword':
                return []
    else:
        raise PreventUpdate

#~~~~~ Fill page content
@app.callback(
[
    Output('div-livefeed-tweets', 'children'),
    Output('div-livefeed-loadmore-button', 'style'),
    Output('label-livefeed-loadmore-page', 'children')
],
[
    Input('div-livefeed-secret-main', 'children'),    
    Input('div-livefeed-secret-filter', 'children'),   
    Input('div-livefeed-secret-search', 'children'),
    Input('button-livefeed-loadmore', 'n_clicks'),
],
[
    State('div-livefeed-tweets', 'children'),
    State('label-livefeed-loadmore-page', 'children')
])
def populate_feed(main_data, filter_data, search_data, loadmore_clicks, div_tweets, loadmore_page):
    ctx = callback_context
    if ctx.triggered:
        ctx_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if ctx_id == 'div-livefeed-secret-main':
            data = main_data
            factor = 0
            div_tweets = []
        elif ctx_id == 'div-livefeed-secret-filter':
            data = search_data if search_data else filter_data
            factor = 0
            div_tweets = []
        elif ctx_id == 'div-livefeed-secret-search':
            data = search_data if search_data else (filter_data if filter_data else main_data)
            factor = 0
            div_tweets = []
        else:
            data = search_data if search_data else (filter_data if filter_data else main_data)
            if search_data:
                print('search data available...')
            else:
                if filter_data:
                    print('filter data available...')
                else:
                    print('main data available...')
            factor = int(loadmore_page)

        df = pd.read_json(json.loads(data), orient='split')
        df = df.reset_index(drop=True)

        style = dict(display='none')
        item_count = df.shape[0]

        print('ctx_id=' + ctx_id)
        print('factor=' + str(factor))
        print('item_count=' + str(item_count))

        if item_count > 15 * factor:
            cardlist = []
            start = 15 * factor
            stop = (start + 15) if item_count > 15 * (factor + 1) else item_count

            for i in range(start, stop):
                prob = df.at[i, 'prob_is_disaster']
                if prob >= 0.5:
                    cardlist.append(format_good_tweet_card(df, i))
                else:
                    cardlist.append(format_bad_tweet_card(df, i))

            if item_count > 15 + 15 * factor:
                style = dict(display='block')

            print('cardlist_len=' + str(len(cardlist)))
            print('style=' + str(style))

            div_tweets.append(html.Div(dbc.CardColumns(cardlist)))

            return div_tweets, style, str(factor + 1)
        else:
            return noresults_layout, style, str(factor)
    else:
        raise PreventUpdate


#~~~~~ Control search badge
@app.callback(
[
    Output('label-livefeed-search-keyword', 'children'),
    Output('div-livefeed-search-filter', 'style'),
    Output('input-livefeed-search-keyword', 'value')
],
[
    Input('input-livefeed-search-keyword', 'value'),    
    Input('badge-livefeed-search-filter', 'n_clicks'),
])
def control_searchbadge(keyword, n_clicks):
    ctx = callback_context
    if ctx.triggered:
        ctx_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if ctx_id == 'input-livefeed-search-keyword' and keyword != '':
            return keyword, dict(display='block'), keyword
        else:
            return '', dict(display='none'), ''
    else:
        raise PreventUpdate

#~~~~~ Display tweet count
@app.callback(
    Output('label-livefeed-results-count', 'children'),
[
    Input('div-livefeed-secret-main', 'children'), 
    Input('div-livefeed-secret-filter', 'children'),
    Input('div-livefeed-secret-search', 'children'),  
])
def count_tweets(main_data, filter_data, search_data):
    ctx = callback_context
    if ctx.triggered:
        ctx_id = ctx.triggered[0]["prop_id"].split(".")[0]
        label = ''

        if ctx_id == 'div-livefeed-secret-main':
            data = main_data
            df = pd.read_json(json.loads(data), orient='split')
            item_count = df.shape[0]
            return ['All ' + pbnj2.get_pretty_int(item_count) + ' tweets']
        elif ctx_id == 'div-livefeed-secret-filter':
            data = search_data if search_data else (filter_data if filter_data else main_data)
            df = pd.read_json(json.loads(data), orient='split')
            item_count = df.shape[0]
            return [pbnj2.get_pretty_int(item_count) + ' matching tweet' + ('' if item_count == 1 else 's')]
        elif ctx_id == 'div-livefeed-secret-search':
            data = search_data if search_data else (filter_data if filter_data else main_data)
            df = pd.read_json(json.loads(data), orient='split')
            item_count = df.shape[0]
            return [pbnj2.get_pretty_int(item_count) + ' matching tweet' + ('' if item_count == 1 else 's')]            
    else:
        raise PreventUpdate
