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

page_help_hotlines = dbc.Container(className='bg-secondary', fluid=True, children=[
    dbc.Container(className='py-4 bg-light', children=[
        html.Section(className='mb-4', children=[
            html.H2('Mental health support'),
            html.P(
            '''
                In an effort to reduce the adverse effects to our users' mental health as caused
                by continued browsing of disaster-related tweets, which are mostly of depressing
                nature, we provide a list of organizations providing mental health support services
                down below:
            '''
            ),
            dbc.ListGroup(children=[
                dbc.ListGroupItem([
                    dbc.ListGroupItemHeading([      
                        dcc.Link('BounceBack', href='https://bouncebackontario.ca/')
                    ]),
                    dbc.ListGroupItemText(
                    '''
                        A free, guided self-help program that’s effective in helping people aged 15
                        and up who are experiencing mild-to-moderate anxiety or depression, or may
                        be feeling low, stressed, worried, irritable or angry.
                    '''
                    ),
                ]),
                dbc.ListGroupItem([
                    dbc.ListGroupItemHeading('Crisis Services Canada (1-833-456-4566)'),
                    dbc.ListGroupItemText(
                    '''
                        Suicide prevention and support.
                    '''
                    ),
                ]),
                dbc.ListGroupItem([
                    dbc.ListGroupItemHeading([      
                        dcc.Link('Distress and Crisis Ontario', href='http://www.dcontario.org/')
                    ]),
                    dbc.ListGroupItemText(
                    '''
                        Distress Centres (DC’s) across Ontario offer support and a variety of services
                        to their communities. At a DC you can find a listening ear for lonely, depressed,
                        and/or suicidal people, usually 24 hours a day, seven days a week. The website
                        also offers a chat function.
                    '''
                    ),                    
                ]),
                dbc.ListGroupItem([
                    dbc.ListGroupItemHeading('Good2Talk Helpline (1-866-925-5454 or text GOOD2TALKON to 686868)'),
                    dbc.ListGroupItemText(
                    '''
                        Ontario’s 24/7 helpline for postsecondary students.
                    '''
                    ),
                ]),
                dbc.ListGroupItem([
                    dbc.ListGroupItemHeading('Hope for Wellness Help Line (1-855-242-3310)'),
                    dbc.ListGroupItemText(
                    '''
                        Offers immediate mental health counselling and crisis intervention to all Indigenous
                        peoples across Canada. Phone and chat counselling is available in English, French,
                        Cree, Ojibway and Inuktitut.
                    '''
                    ),
                ]),
                # dbc.ListGroupItem([
                #     dbc.ListGroupItemHeading('Assaulted Women’s Helpline (1-866-863-0511)'),
                #     dbc.ListGroupItemText(
                #     '''
                #         24-hour telephone and TTY crisis line for all women in Ontario who have experienced
                #         any form of abuse.
                #     '''
                #     ),
                # ]),
                # dbc.ListGroupItem([
                #     dbc.ListGroupItemHeading('Seniors Safety Line (1-866-299-1011)'),
                #     dbc.ListGroupItemText(
                #     '''
                #         Provided by Elder Abuse Ontario, the Seniors Safety Line provides contact and
                #         referral information for local agencies across the province that can assist in
                #         cases of elder abuse.
                #     '''
                #     ),
                # ]),
                # dbc.ListGroupItem([
                #     dbc.ListGroupItemHeading([      
                #         dcc.Link('LGBT Youthline Ontario', href='https://www.youthline.ca/'),
                #         html.Span(' (647-694-4275)')
                #     ]),
                #     dbc.ListGroupItemText(
                #     '''
                #         Ontario-wide peer-support for lesbian, gay bisexual, transgender, transsexual,
                #         two-spirited, queer and questioning young people.
                #     '''
                #     ),                    
                # ]),                               
            ]),
        ]),
        html.Section([
            html.H2('Donations'),
            html.P(
                '''
                To help provide aid and relief to disaster-stricken areas, users can setup and seek financial
                aid on behalf of those communities through the following fund-raising services:
                '''
            ),
            dbc.ListGroup(children=[
                dbc.ListGroupItem([
                    dbc.ListGroupItemHeading([      
                        dcc.Link('GoFundMe', href='https://www.gofundme.com/start/emergency-fundraising')
                    ]),
                    dbc.ListGroupItemText(
                    '''
                        GoFundMe is an American for-profit crowdfunding platform that allows people to raise
                        money for events ranging from life events such as celebrations and graduations to
                        challenging circumstances like accidents and illnesses.
                    '''
                    ),
                ]),
            ])            
        ])
    ])
])

layout = page_help_hotlines

#-------------------------------------------------------------------------------------------------
# Callbacks