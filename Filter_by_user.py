# Displays the Tweets tweeted by the user in real-time. 

from ssl import SSLError
import re
import time
from requests.exceptions import Timeout, ConnectionError
from urllib3.exceptions import ReadTimeoutError, ProtocolError
import json
import tweepy
import sqlite3
import logging
global api

consumer_key="Insert_consumer_key_here"
consumer_secret="Insert_consumer_secret_here"
access_token="Insert_access_token_here"
access_token_secret="Insert_access_token_secret_here"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
if (api):
    print("Login Success")
else:
    print("Failed")

class TweetStreamListener(tweepy.StreamListener):
    def on_data(self,data):
        #dumping json data
        tweet=json.loads(data)
        try:
                def from_creator(data):
                    if hasattr(data, 'retweeted_status'):
                        return False
                    else:
                        return True
                if from_creator(data):     
                    # To filter out retweets and to access tweets greater than 140 characters in length.
                    if  not tweet["text"].startswith('RT'):
                        if tweet.get("extended_tweet"):
                            text = str(tweet['extended_tweet']["full_text"])
                        else:
                            text= str(tweet["text"])
                        print(text)
                return True
                
        except Exception as e:
            print(e)
            return True
        
if __name__ == '__main__':
    print("start \n")
    # Run the stream!
    l = TweetStreamListener()
    stream = tweepy.Stream(auth, l,tweet_mode='extended')
    # Filtering
    while not stream.running:
        try:
            logging.info("Started listening to twitter stream...")
            stream.filter(follow=['insert_twitter_id_here'])             
        except(ProtocolError, AttributeError):
            continue
        except(Timeout, SSLError, ReadTimeoutError, ConnectionError) as e:
            logging.warning("Network error occurred.", str(e))
        except Exception as e:
            logging.error("Unexpected error.", e)
        finally:
            logging.info("Stream has crashed.")
    logging.critical("Somehow zombie has escaped.")

