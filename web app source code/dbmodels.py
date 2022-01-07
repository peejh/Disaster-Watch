from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, Float, DateTime, BigInteger, Boolean, Text, String, SmallInteger

Base = declarative_base()


class Tweet(Base):
	__tablename__ = 'tweet'

	id = Column(BigInteger, primary_key=True)
	id_str = Column(String(length=25), nullable=False)
	created_at = Column(DateTime, nullable=False)
	last_tweeted_at = Column(DateTime, nullable=False)
	user_id = Column(BigInteger, nullable=False)
	user_id_str = Column(String(length=25), nullable=False)
	user_name = Column(Text, nullable=False)
	user_screen_name = Column(Text, nullable=False)
	user_profile_pic_url = Column(Text, nullable=False)
	user_verified = Column(Boolean, nullable=False)
	user_fr_count = Column(Integer)
	user_fo_count = Column(Integer)
	user_location = Column(String)
	user_coords_long = Column(Float(precision=4))
	user_coords_lat = Column(Float(precision=4))
	text = Column(Text, nullable=False)
	source = Column(Text)
	quoted_status = Column(Boolean, nullable=False)
	reply_status = Column(Boolean, nullable=False)
	reply_count = Column(Integer)
	retweet_count = Column(Integer)
	favorite_count = Column(Integer)
	lang = Column(String(length=2))
	coordinates_long = Column(Float(precision=4))
	coordinates_lat = Column(Float(precision=4))
	place_full_name = Column(Text)
	place_country_code = Column(String(length=2))
	prob_is_disaster = Column(Float(precision=4), nullable=False)
	url_web_view = Column(String, nullable=False)
	url_embed_view = Column(String, nullable=False)


class Hashtag(Base):
	__tablename__ = 'hashtag'

	index = Column(Integer, primary_key=True, autoincrement=True)
	recorded_at = Column(DateTime, nullable=False)
	tweet_id = Column(BigInteger, nullable=False)
	word = Column(String, nullable=False)


class Tweed(Base):
	__tablename__ = 'tweed'

	id = Column(BigInteger, primary_key=True)
	created_at = Column(DateTime, nullable=False)
	text = Column(Text, nullable=False)
	prob_is_disaster = Column(Float(precision=4), nullable=False)
	url_web_view = Column(String, nullable=False)


class Place(Base):
	__tablename__ = 'place'

	nomin_id = Column(BigInteger, primary_key=True)
	osm_id = Column(BigInteger, nullable=False)
	city = Column(String)
	county = Column(String)
	state = Column(String)
	country = Column(String, nullable=False)
	iso2 = Column(String(length=2))
	lon = Column(Float(precision=8), nullable=False)
	lat = Column(Float(precision=8), nullable=False)
	zoom = Column(Float(precision=8), nullable=False)
	bb_min_lat = Column(Float(precision=8), nullable=False)
	bb_max_lat = Column(Float(precision=8), nullable=False)
	bb_min_lon = Column(Float(precision=8), nullable=False)
	bb_max_lon = Column(Float(precision=8), nullable=False)
	bb_center_lat = Column(Float(precision=8), nullable=False)
	bb_center_lon = Column(Float(precision=8), nullable=False)
	display = Column(String)
	display_ascii = Column(String, nullable=False)
	city_ascii = Column(String)
	osm_type = Column(String, nullable=False)
	place_class = Column(String, nullable=False)
	place_type = Column(String, nullable=False)
	importance = Column(Float(precision=8), nullable=False)
