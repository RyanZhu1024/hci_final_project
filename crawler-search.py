import tweepy
from tweepy import OAuthHandler
from tweepy import Cursor
import json

consumer_key = 'tFPPuCnXFfCaXrzZGX3VxuiAq'
consumer_secret = '7161pEppFf4je7EUfHdUJZMJ6CP2rXJxpYAMEslfwAjwnEyppC'
access_token = '1469837503-F7iiKxptuVpwSIjImARRKVLuUPlQw1kzzERzV06'
access_secret = 'Z7OJZSTH7C2FfETuCXpaFCdrWsxAa9AzhBw1HmynR1sGS'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

PAGES = 200

data = Cursor(api.search, q='#threebodyproblem', count=100, result_type='recent', lang='en').items()

with open('threebody.txt', 'w') as f:
    for tweet in data:
        f.write(json.dumps(tweet._json))
        f.write('\n')

