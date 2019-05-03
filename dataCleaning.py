# -*- coding: utf-8 -*-
import time
import json
import tweepy
import couchdb
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

# initialize database
couch = couchdb.Server("http://100.103.123.77:5984/")
database= couch['temp']

# initialize apis
key_secret_pairs=[];
key_secret_pairs.append(('rcFJ0DzhHSDvTfgHK49WMCc9S','LZdhAUDVvnWcHHxUXTzYQF2f57KrNfmtEZHCmKzNZjxxsuG0Bp'))
api_s=[]
for key_secret_pair in key_secret_pairs:
    auth = tweepy.OAuthHandler(key_secret_pair[0], key_secret_pair[1])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    api_s.append(api)

# load boundary file
boundaryJS = json.load(open('data/melb.json'))

def cor2suburb(coordinates, boundaryJS):
    for ele in boundaryJS["features"]:
        if ele['geometry']['type']=='Polygon':
            if Polygon(ele["geometry"]["coordinates"][0]).contains(Point(coordinates)):
                return ele['properties']["SA2_NAME16"]
        elif ele['geometry']['type']=='MultiPolygon':
            for polygon in ele['geometry']['coordinates']:
                if Polygon(polygon[0]).contains(Point(coordinates)):
                    return ele['properties']["SA2_NAME16"]
    return None

def do100tweets(database, tweet_list):
    # print(len(tweet_list))
    for tweet in tweet_list[1:]:
        tweetJS=tweet._json;
        if tweetJS["place"]:
            if tweetJS["place"]["place_type"]=="neighborhood":
                database.save({"suburb": tweetJS["place"]["name"], "doc": tweetJS})
                # print(tweetJS["place"]["name"])
                continue
        if tweetJS["coordinates"]:
            long,lat = tweetJS["coordinates"]["coordinates"][0],tweetJS["coordinates"]["coordinates"][1]
            sub = cor2suburb([long,lat],boundaryJS)
            # print([long, lat, sub])
            if sub!=None:
                database.save({"suburb":sub,"doc":tweetJS})

# newer tweet has bigger id
# api.search(since_id=null, max_id=newest_id, count=min(100,count))
# return [maxID, down to about_count]
# or [max_id, down to the id just bigger than since_id]
# or [max_id, least_id within 10 days] when reaching the last-10-day limit
# each api can call search about 450 times within 15 mins, otherwise auto-wait least seconds until the next 15 mins
tweet_list =api_s[-1].search(max_id =1123893169257631749,geocode="-37.999250,144.997395,57km", count=100)
maxID = tweet_list[0].id
while len(tweet_list)>1:
    for api in api_s:
        tweet_list = api.search(max_id=maxID, geocode="-37.999250,144.997395,57km", count=100);
        try: do100tweets(database, tweet_list)
        except: pass
        maxID  = tweet_list[-1].id




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


