import tweepy
import json
import couchdb
import time
import datetime
import unicodedata
# consumer_key=''
# consumer_secret = ''
# access_token = ''
# access_token_secret = ''

consumer_key = 'v0972w9aptiA8Dzm97sGFykPY'
consumer_secret = 'e9P4IMHyWEIwqwKiYVu4qDwXLMBooockFeqs5lwkjhCvJ0efle'
access_key = '988266868828815360-LUDs2XCggWF57JVCZpOSvDTyxYNxEcg'
access_secret = 'GdkzCMPkAFhJU6jHfr15ZD4TmSETTW41RQLxp3lNODoVL'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# server = "http://100.103.123.77:5984"
# database_name = 'live_tweet'
# couch = couchdb.Server(server)
# database = couch[database_name]

import googlemaps
# file2 = open(r"result.txt","w+")
gmaps = googlemaps.Client(key='AIzaSyBJSHURhn2lPbsK8P1A1TK17XZvC_zTdCg')
gmaps2=googlemaps.client
# gmaps2.reverse_geocode()
# print(gmaps.reverse_geocode((-37.81194167,144.95))[0]['address_components'][2]['long_name'])



# In this example, the handler is time.sleep(15 * 60),
# but you can of course handle it in any way you want.

f = open('5_1to.json', 'rb')
i=0
line = f.readline()
while line:
    try:
        jtweet=json.loads(line.decode().strip().strip(','))
        if jtweet["doc"]["geo"] != None:
            print (jtweet["doc"]["geo"]["coordinates"][0])
            print (jtweet["doc"]["geo"]["coordinates"][1])
            print (api.reverse_geocode(jtweet["doc"]["geo"]["coordinates"][0],jtweet["doc"]["geo"]["coordinates"][1]))
    except:
        pass
    line = f.readline()

# print (api.reverse_geocode(-37.81194167,144.95))


# def limit_handled(cursor):
#     while True:
#         try:
#             yield cursor.next()
#         except tweepy.RateLimitError:
#             time.sleep(15 * 60)
#
# for status in limit_handled(tweepy.Cursor(api.search,q="*").items()):
#         print (status)


# file2 = open(r"result.txt","w+")



# print (c.next())
# b=c.next()
# print (json.dumps(b._json))
# file2.write(str(c.next()))

# c = tweepy.Cursor(api.search,q="",geocode="-37.9994,144.5937,99km").items()
# k=0
# while True:
#     try:
#         tweet = c.next()
#         print (tweet)
#         # database.save({"tweet_json": json.loads(json.dumps(tweet._json))})
#         k+=1
#     except tweepy.TweepError:
#         print("break from error")
#         break
#     except StopIteration:
#         print("break from stop")
#         break
# print (k)



# try:
#     for status in c:
#         print (status)
# except tweepy.TweepError:

# try:
#     print(status)
# except tweepy.TweepError:
#     break

# while True:
#     try:
#         tweet = c.next()
#         print(tweet)
#         # Insert into db
#     except tweepy.TweepError:
#         print ("too many requests")
#         # time.sleep(60 * 15)
#         break;
#     except StopIteration:
#         break


# search_results = api.search(q="haha",since= "2019-01-24 05:30",count=1000)
# for ele in search_results:
#     print (type(ele))
    # {"tweet_data": json_data}
# search_results=search_results.next()

# database.save({"a": 1,"b": 2})
# database.save({"a": 1,"b": 2})


# class MyStreamListener(tweepy.StreamListener):
#     num_tweets = 0
#     # def on_status(self, data):
#     #     self.num_tweets+=1;
#     #     if self.num_tweets > 20:
#     #         return False
#
#     def on_data(self, data):
#
#         if self.num_tweets > 3500:
#             return False
#         jsontweet=json.loads(data)
#         # if (jsontweet['retweeted']==False) and (not jsontweet["text"].startswith("RT ")):
#         self.num_tweets += 1;print (self.num_tweets)
#         # print(jsontweet)
#         database.save({"tweet_json": jsontweet})
#
# myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())
# myStream.filter(track=["*"],locations=[144.5937,-37.9994,145.4013,-37.5113])


# result_type="recent",include_entities=True,count=1,
# c = tweepy.Cursor(api.search, q="haha",since= "2018-01-24 05:30").items()
# for tweet in c:
#     print (tweet)
# c=c.next()



