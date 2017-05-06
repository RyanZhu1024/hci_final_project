import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

consumer_key = 'tFPPuCnXFfCaXrzZGX3VxuiAq'
consumer_secret = '7161pEppFf4je7EUfHdUJZMJ6CP2rXJxpYAMEslfwAjwnEyppC'
access_token = '1469837503-F7iiKxptuVpwSIjImARRKVLuUPlQw1kzzERzV06'
access_secret = 'Z7OJZSTH7C2FfETuCXpaFCdrWsxAa9AzhBw1HmynR1sGS'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


class MyListener(StreamListener):

    def on_data(self, data):
        try:
            with open('test-data.json', 'a') as f:
                print(data)
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return True

    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#Rockets', 'Rockets'])
