from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json

ckey = '9Ahv1EMvtIxy1ykA1JKRIA'
csecret = 'Yc7kQWDqxPn4ImYAAb1C2OG8hqORcXu9lXhdgo9BpA'
atoken = '170438473-CGNP9P253TedqYJoD9W1GPN2ZE99K3Sbzhix0xkc'
asecret = 'AA1ewSLtoL7Knxj1m2kVHULyF2GTvCscUJ5rpwLncWjN7'


class listener(StreamListener):
    def on_data(self, data):
        try:
            # print(data)
            all_data = json.loads(data)
            #tweet = data.split(',"text":"')[1].split('","source')[0]
            tweet = all_data["text"]
            # timed = all_data["created_at"]
            print(tweet)
            # saveThis = str(time.time())+ '::' + tweet
            saveThis = tweet
            saveFile = open('twitDB3.txt', 'a')
            saveFile.write(saveThis)
            saveFile.close
            
            return True
        except BaseException as e:
            print ('failed ondata,', str(e))
            time.sleep(5)
    
    def on_error(self, status):
        print (status)

try:
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    twitterStream = Stream(auth, listener())
    twitterStream.filter(track=['$AAPL'])
except BaseException as e:
    print(e)

