from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import RateLimitError
 
import numpy as np
import pandas as pd
import re
import time
import json
from unidecode import unidecode
from datetime import datetime
import ktrain
from geopy.geocoders import Nominatim

from pbnj2 import *
from dbcrud import engine
from dbcrud import Session
from dbmodels import Tweet
from dbmodels import Hashtag
from dbmodels import Tweed


class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return auth


class TwitterStreamer():

    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()    

    def stream_tweets(self, keywords, processor):
        listener = TwitterListener(processor)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)

        stream.filter(track=keywords)


class TwitterListener(StreamListener):

    def __init__(self, processor):
        self.processor = processor

    def on_data(self, data):
        try:
            # print(data)
            data = json.loads(data)

            #-----------------------------------------------------
            # if retweet
            #     if retweet not in db
            #         process retweet
            #     else
            #         update existing tweet entry
            # else if quote
            #     if quote not in db
            #         process quote
            #     else
            #         update existing tweet entry
            #     process current tweet with is_quote flag
            # else if reply
            #     process current tweet with is_reply flag
            # else
            #     process current tweet
            #
            
            if 'retweeted_status' in data:
                retweet = data['retweeted_status']
                retweet_id = retweet['id']
                if processor.is_tweet_exist(retweet_id):
                    print('Updating Retweet...')
                    time_updated = data['created_at']
                    processor.update_tweet(retweet, time_updated)
                else:
                    print('Processing Retweet...')
                    processor.process_tweet(retweet)
            elif 'quoted_status' in data:
                quote = data['quoted_status']
                quote_id = quote['id']
                if processor.is_tweet_exist(quote_id):
                    print('Updating Quoted tweet...')
                    time_updated = data['created_at']
                    processor.update_tweet(quote, time_updated)
                else:
                    print('Processing Quoted tweet...')
                    processor.process_tweet(quote)
                print('Processing Quote...')
                processor.process_tweet(data, is_quote=True)
            elif data.get('in_reply_to_status_id') is not None:
                processor.process_tweet(data, is_reply=True)
            else:
                processor.process_tweet(data)

            print('\n\n')
            return True
        except BaseException as e:
            print("Error on_data {}\n\n".format(str(e)))
        return True
          
    def on_error(self, status):
        print(status)
        if status == 420:   # rate limit
            return False    # close stream


# Probably not needed
class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth, wait_on_rate_limit=True)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []     
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


class TweetProcessor:

    def __init__(self):
        self.session = None
        self.predictor = ktrain.load_predictor('model')
        self.geocoder = Nominatim(user_agent='YU-ENG4K-TeamP-stream')

    def process_tweet(self, data, is_reply=False, is_quote=False):
        if 'extended_tweet' in data:
            text = data['extended_tweet']['full_text']
        else:
            text = data['text']       

        prob_is_disaster = 0.0
        [_, prob_is_disaster] = self.get_predictions(text)

        print(text)
        print(prob_is_disaster)

        #------------------------------------------------------------
        if prob_is_disaster > 0.5:
            print('Saving GOOD tweet...')

            # Gather data
            id = data['id']
            id_str = data['id_str']
            created_at = datetime.strftime(datetime.strptime(data['created_at'],'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
            last_tweeted_at = created_at
            user_id = data['user']['id']
            user_id_str = data['user']['id_str']
            user_name = data['user']['name']
            user_screen_name = data['user']['screen_name']
            user_profile_pic_url = data['user']['profile_image_url_https']
            user_verified = data['user']['verified']
            user_fr_count = data['user']['friends_count']
            user_fo_count = data['user']['followers_count']
            # retweeted_status = is_retweet
            quoted_status = is_quote
            reply_status = is_reply
            reply_count = data['reply_count']
            retweet_count = data['retweet_count']
            favorite_count = data['favorite_count']
            lang = data['lang']
            source = re.findall(r'<.+>(.*?)<.+>', data['source'])[0] if not None else None

            user_location = None
            user_coords_long = None
            user_coords_lat = None
            if data['user'].get('location') is not None:
                [user_location, user_coords_long, user_coords_lat] = self.get_place_info(data['user']['location'])

            [coordinates_long, coordinates_lat] = data['coordinates']['coordinates'] if data.get('coordinates') is not None else [None, None]

            if data.get('place') is not None:
                place_full_name = data['place']['full_name']
                place_country_code = data['place']['country_code']
                if coordinates_long is None:
                    [_, coordinates_long, coordinates_lat] = self.get_place_info(place_full_name)
            elif coordinates_long is not None:
                # do reverse lookup
                [place_full_name, place_country_code] = self.get_place_info_from_coords(coordinates_long, coordinates_lat)
            else:
                place_full_name = None
                place_country_code = None

            url_web_view = 'https://twitter.com/i/web/status/' + id_str
            url_embed_view = 'https://twitter.com/' + user_screen_name + '/status/' + id_str

            # Save tweet
            tweet = Tweet(
                id = id,
                id_str = id_str,
                created_at = created_at,
                last_tweeted_at = last_tweeted_at,
                user_id = user_id,
                user_id_str = user_id_str,
                user_name = user_name,
                user_screen_name = user_screen_name,
                user_profile_pic_url = user_profile_pic_url,
                user_verified = user_verified,
                user_fr_count = user_fr_count,
                user_fo_count = user_fo_count,
                user_location = user_location,
                user_coords_long = user_coords_long,
                user_coords_lat = user_coords_lat,
                text = text,
                source = source,
                quoted_status = quoted_status,
                reply_status = reply_status,
                reply_count = reply_count,
                retweet_count = retweet_count,
                favorite_count = favorite_count,
                lang = lang,
                coordinates_long = coordinates_long,
                coordinates_lat = coordinates_lat,
                place_full_name = place_full_name,
                place_country_code = place_country_code,
                prob_is_disaster = prob_is_disaster,
                url_web_view = url_web_view,
	            url_embed_view = url_embed_view
            )

            self.session = Session()
            self.session.add(tweet)
            self.session.commit()
            self.session.close()

            #--------------------------------------------------------
            tags = data['entities']['hashtags']

            if tags:
                hashtags = {str(rec['text']).lower() for rec in tags}

                for word in hashtags:
                    hashtag = Hashtag(
                        recorded_at = created_at,
                        tweet_id = id,
                        word = word
                    )

                    self.session = Session()
                    self.session.add(hashtag)
                    self.session.commit()
                    self.session.close()
        
        #------------------------------------------------------------
        else:
            print('Saving BAD tweet...')

            # Gather data
            id = data['id']
            created_at = datetime.strftime(datetime.strptime(data['created_at'],'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
            url_web_view = 'https://twitter.com/i/web/status/' + str(id)

            # Save tweet
            tweed = Tweed(
                id = id,
                created_at = created_at,
                text = text,
                prob_is_disaster = prob_is_disaster,
                url_web_view = url_web_view
            )

            self.session = Session()
            self.session.add(tweed)
            self.session.commit()
            self.session.close()            

    def update_tweet(self, data, time_updated):
        tweet = self.session.query(Tweet).filter(Tweet.id == data['id']).first()
        if tweet:
            print('Updating GOOD tweet...')
            tweet.last_tweeted_at = time_updated
            # tweet.user_fr_count = data['user']['friends_count']       # doesn't make sense until we have a User table
            # tweet.user_fo_count = data['user']['followers_count']     # doesn't make sense until we have a User table
            tweet.reply_count = data['reply_count']
            tweet.retweet_count = data['retweet_count']
            tweet.favorite_count = data['favorite_count']
            self.session = Session()
            self.session.commit()
            self.session.close()
        else:
            print('Ignoring BAD tweet update...')

    def get_predictions(self, text):
        return self.predictor.predict(text, return_proba=True).tolist()

    def get_place_info(self, place):
        place_geocode = self.geocoder.geocode(place)
        if place_geocode is not None:
            return [place_geocode.raw['display_name'], place_geocode.longitude, place_geocode.latitude]
        else:
            return [None, None, None]

    def get_place_info_from_coords(self, lon, lat):
        coords = lat + ', ' + lon
        reverse_geocode = self.geocoder.reverse(coords)
        if reverse_geocode is not None:
            address = reverse_geocode.raw['address']
            location = address['city'] + ', ' + address['state'] + ', ' + address['country']
            country_code = address['country_code']
            return [location, str(country_code).upper()]
        else:
            return [None, None]

    def is_tweet_exist(self, tweet_id):
        self.session = Session()
        tweet_found = self.session.query(Tweet).filter(Tweet.id == tweet_id).first()
        bad_tweet_found = self.session.query(Tweed).filter(Tweed.id == tweet_id).first()
        self.session.close()
        if tweet_found is None and bad_tweet_found is None:
            return False
        return True


if __name__ == '__main__':

    # keywords = CRISIS_LEXICON
    keywords = TOP100_LEXICON
    # keywords = MAJOR_EVENTS_LEXICON
    # keywords = SIMPLE_LEXICON
    processor = TweetProcessor()

    while True:
        try:
            stream = TwitterStreamer()
            stream.stream_tweets(keywords, processor)
        except Exception as e:
            print("{} Error: Connection Dropped\n".format(time.strftime('%m/%d/%Y %H:%M:%S')))
            print(e.__doc__)
            if e == RateLimitError:
                print('Rate limit reached. Waiting for 15 mins...')
                time.sleep((15*60)+1) # wait 15 mins
            print("Re-establishing Connection...")
 