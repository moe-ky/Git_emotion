from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json

ckey = '9Ahv1EMvtIxy1ykA1JKRIA'
csecret = 'Yc7kQWDqxPn4ImYAAb1C2OG8hqORcXu9lXhdgo9BpA'
atoken = '170438473-CGNP9P253TedqYJoD9W1GPN2ZE99K3Sbzhix0xkc'
asecret = 'AA1ewSLtoL7Knxj1m2kVHULyF2GTvCscUJ5rpwLncWjN7'


def name_of(entity):
    global track
    track = entity
    symbol(track)

try:
    def symbol(name):
        to_track = name
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        twitter_stream = Stream(auth, Listener())
        twitter_stream.filter(track=[to_track], languages=['en', 'en-gb'])
except BaseException as e:
    print(e)


class Listener(StreamListener):
    def on_data(self, data):
        try:
            all_data = json.loads(data)
            tweet = all_data["text"]
            time_of = time.strftime("%H")
            date_of = time.strftime("%d_%m")
            path = "C:/Users/MOYIN/Desktop/Dissertation/Development/WebSc/Tracker/" + track + "/" + track + "_" \
                   + date_of+"_"+time_of+".json"

            with open(path, 'a') as f:
                    json.dump(all_data, f)
                    f.write("\n")
                    print(tweet.encode("utf-8"))
            return True

        except BaseException as e:
            print('failed on_data: %s,' % str(e))
            time.sleep(2)
        return True

    def on_status(self, status):
        try:
            print(status)
        except BaseException as e:
            print('failed on_data: %s,' % str(e))
            time.sleep(5)

    def on_error(self, status):
        print(status)
        return True

