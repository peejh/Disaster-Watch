import dash
import dash_bootstrap_components as dbc

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


#-------------------------------------------------------------------------------------------------
# Initialize

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    {
        'href': 'https://use.fontawesome.com/releases/v5.15.2/css/all.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-vSIIfh2YWi9wW0r9iZe7RJPrKwp6bG+s9QZMoITbCckVJqGCCRhc+ccxNcdpHuYu',
        'crossorigin': 'anonymous'
    },
    {
        'href': 'https://fonts.googleapis.com/css2?family=Monoton&display=swap',
        'rel': 'stylesheet'
    }
]

server = Flask(__name__)
app = dash.Dash(__name__, title='Disaster Watch', update_title=None,
                server=server, suppress_callback_exceptions=True, 
                external_stylesheets=external_stylesheets,
                meta_tags=[{'name':'viewport',
                            'content':'width=device-width, initial-scale=1.0'}]
                )


#-------------------------------------------------------------------------------------------------
# Database setup

app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.server.config["SQLALCHEMY_DATABASE_URI"] = 'postgres+psycopg2://DBADMIN_USERNAME:DBADMIN_PW@localhost:5432/postgres'

db = SQLAlchemy(app.server, engine_options=dict(pool_size=25, max_overflow=25))

class Tweet(db.Model):
    __tablename__ = 'tweet'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    id_str = db.Column(db.String(length=25), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    last_tweeted_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.BigInteger, nullable=False)
    user_id_str = db.Column(db.String(length=25), nullable=False)
    user_name = db.Column(db.Text, nullable=False)
    user_screen_name = db.Column(db.Text, nullable=False)
    user_profile_pic_url = db.Column(db.Text, nullable=False)
    user_verified = db.Column(db.Boolean, nullable=False)
    user_fr_count = db.Column(db.Integer)
    user_fo_count = db.Column(db.Integer)
    user_location = db.Column(db.String)
    user_coords_long = db.Column(db.Float(precision=4))
    user_coords_lat = db.Column(db.Float(precision=4))
    text = db.Column(db.Text, nullable=False)
    source = db.Column(db.Text)
    quoted_status = db.Column(db.Boolean, nullable=False)
    reply_status = db.Column(db.Boolean, nullable=False)
    reply_count = db.Column(db.Integer)
    retweet_count = db.Column(db.Integer)
    favorite_count = db.Column(db.Integer)
    lang = db.Column(db.String(length=2))
    coordinates_long = db.Column(db.Float(precision=4))
    coordinates_lat = db.Column(db.Float(precision=4))
    place_full_name = db.Column(db.Text)
    place_country_code = db.Column(db.String(length=2))
    prob_is_disaster = db.Column(db.Float(precision=4), nullable=False)
    url_web_view = db.Column(db.String, nullable=False)
    url_embed_view = db.Column(db.String, nullable=False)

    def __init__(id, id_str, created_at, last_tweeted_at, 
                 user_id, user_id_str, user_name, user_screen_name, 
                 user_profile_pic_url, user_verified, user_fo_count, user_fr_count,
                 user_location, user_coords_long, user_coords_lat,
                 text, source, quoted_status, reply_status,
                 reply_count, retweet_count, favorite_count, lang, 
                 coords_long, coords_lat, place_full_name, place_country_code, 
                 prob_is_disaster, url_web_view, url_embed_view):
        self.id = id
        self.id_str = id_str
        self.created_at = created_at
        self.last_tweeted_at = last_tweeted_at
        self.user_id = user_id
        self.user_id_str = user_id_str
        self.user_name = user_name
        self.user_screen_name = user_screen_name
        self.user_profile_pic_url = user_profile_pic_url
        self.user_verified = user_verified
        self.user_fr_count = user_fr_count
        self.user_fo_count = user_fo_count
        self.user_location = user_location
        self.user_coords_long = user_coords_long
        self.user_coords_lat = user_coords_lat
        self.text = Text
        self.source = source
        self.quoted_status = quoted_status
        self.reply_status = reply_status
        self.reply_count = reply_count
        self.retweet_count = retweet_count
        self.favorite_count = favorite_count
        self.lang = lang
        self.coordinates_long = coords_long
        self.coordinates_lat = coords_lat
        self.place_full_name = place_full_name
        self.place_country_code = place_country_code
        self.prob_is_disaster = prob_is_disaster
        self.url_web_view = url_web_view
        self.url_embed_view = url_embed_view

class Hashtag(db.Model):
    __tablename__ = 'hashtag'

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recorded_at = db.Column(db.DateTime, nullable=False)
    tweet_id = db.Column(db.BigInteger, nullable=False)
    word = db.Column(db.String, nullable=False)

    def __init__(index, recorded_at, tweet_id, word):
        self.index = index
        self.recorded_at = recorded_at
        self.tweet_id = tweet_id
        self.word = word

class Tweed(db.Model):
    __tablename__ = 'tweed'

    id = db.Column(db.BigInteger, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=False)
    prob_is_disaster = db.Column(db.Float(precision=4), nullable=False)
    url_web_view = db.Column(db.String, nullable=False)

    def __init__(created_at, text, prob_is_disaster, url_web_view):
        self.created_at = created_at
        self.text = text
        self.prob_is_disaster = prob_is_disaster
        self.url_web_view = url_web_view

class Place(db.Model):
    __tablename__ = 'place'

    nomin_id = db.Column(db.BigInteger, primary_key=True)
    osm_id = db.Column(db.BigInteger, nullable=False)
    city = db.Column(db.String)
    county = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String, nullable=False)
    iso2 = db.Column(db.String(length=2))
    lon = db.Column(db.Float(precision=8), nullable=False)
    lat = db.Column(db.Float(precision=8), nullable=False)
    zoom = db.Column(db.Float(precision=8), nullable=False)
    bb_min_lat = db.Column(db.Float(precision=8), nullable=False)
    bb_max_lat = db.Column(db.Float(precision=8), nullable=False)
    bb_min_lon = db.Column(db.Float(precision=8), nullable=False)
    bb_max_lon = db.Column(db.Float(precision=8), nullable=False)
    bb_center_lat = db.Column(db.Float(precision=8), nullable=False)
    bb_center_lon = db.Column(db.Float(precision=8), nullable=False)
    display = db.Column(db.String)
    display_ascii = db.Column(db.String, nullable=False)
    city_ascii = db.Column(db.String)
    osm_type = db.Column(db.String, nullable=False)
    place_class = db.Column(db.String, nullable=False)
    place_type = db.Column(db.String, nullable=False)
    importance = db.Column(db.Float(precision=8), nullable=False)

    def __init__(nomin_id, osm_id, city, county, state, country, iso2,
                 lon, lat, zoom, bb_min_lat, bb_max_lat, bb_min_lon, bb_max_lon,
                 bb_center_lat, bb_center_lon, display, display_ascii, city_ascii,
                 osm_type, place_class, place_type, importance):
        self.nomin_id = nomin_id
        self.osm_id = osm_id
        self.city = city
        self.county = county
        self.state = state
        self.country = country
        self.iso2 = iso2
        self.lon = lon
        self.lat = lat
        self.zoom = zoom
        self.bb_min_lat = bb_min_lat
        self.bb_max_lat = bb_max_lat
        self.bb_min_lon = bb_min_lon
        self.bb_max_lon = bb_max_lon
        self.bb_center_lat = bb_center_lat
        self.bb_center_lon = bb_center_lon
        self.display = display
        self.display_ascii = display_ascii
        self.city_ascii = city_ascii
        self.osm_type = osm_type
        self.place_class = place_class
        self.place_type = place_type
        self.importance = importance