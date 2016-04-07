import tweepy
import json
import time

ckey = '9Ahv1EMvtIxy1ykA1JKRIA'
csecret = 'Yc7kQWDqxPn4ImYAAb1C2OG8hqORcXu9lXhdgo9BpA'
atoken = '170438473-CGNP9P253TedqYJoD9W1GPN2ZE99K3Sbzhix0xkc'
asecret = 'AA1ewSLtoL7Knxj1m2kVHULyF2GTvCscUJ5rpwLncWjN7'

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Open/Create a file to append data
time_of = time.strftime("%H")
date_of = time.strftime("%d_%m_%y")
tweetsPerQry = 100  # this is the max the API permits

since_id = 699020055938408448
max_id = 700832236602392579

since = 701555547619856386
maxy = 703368729845960705

# print(tweet.created_at, tweet.id)


def catch(query):
    for tweet in tweepy.Cursor(api.search, q=query, count=tweetsPerQry,since=2016-3-25, lang="en").items():
        ti = tweet.created_at
        # get tweets based on day month and year
        string_time = ti.strftime('%d-%m-%y')
        file_s = "C:/Users/MOYIN/Desktop/Flask/WebSc/Tracker/"+query+"/"+query+"-"+string_time + ".json"
        with open(file_s, 'a') as f:
            json.dump(tweet.text, f)
            print(tweet.text)
            f.write("\n")