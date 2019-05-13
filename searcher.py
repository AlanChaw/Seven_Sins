# -*- coding: utf-8 -*-
import json
import tweepy
import couchdb
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import re

# global variables:
# boundary file - dictionary
boundaryJS = json.load(open('D:/data/melb.json'))
# all suburb names - list
sub_list=[ele['properties']["SA2_NAME16"] for ele in boundaryJS["features"]]
# target database object
database= couchdb.Server("http://10.13.113.161:5984/")['temp3']
# initialize apis
key_secret_pairs=[];
key_secret_pairs.append(('rcFJ0DzhHSDvTfgHK49WMCc9S','LZdhAUDVvnWcHHxUXTzYQF2f57KrNfmtEZHCmKzNZjxxsuG0Bp'))
api_s=[]
for key_secret_pair in key_secret_pairs:
    auth = tweepy.OAuthHandler(key_secret_pair[0], key_secret_pair[1])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    api_s.append(api)

def sub_name_normalisation(input_name):
    for standard_sub in sub_list:
        if input_name.lower() == standard_sub.lower():
            return standard_sub
    for standard_sub in sub_list:
        if input_name.lower() in standard_sub.lower():
            return standard_sub
    for standard_sub in sub_list:
        if input_name.replace(" ", " - ").lower() == standard_sub.lower():
            return standard_sub
    for standard_sub in sub_list:
        if input_name.replace(" ", " - ").lower() in standard_sub.lower():
            return standard_sub
    for standard_sub in sub_list:
        if ('South' not in standard_sub) and ('North' not in standard_sub) and ('West' not in standard_sub) and (
                'East' not in standard_sub):
            new = re.sub(r' South| North| West| East', '', input_name)
            if new.lower() == standard_sub.lower():
                return standard_sub
    for standard_sub in sub_list:
        if ('South' not in standard_sub) and ('North' not in standard_sub) and ('West' not in standard_sub) and (
                'East' not in standard_sub):
            new = re.sub(r' South| North| West| East', '', input_name)
            if new.lower() in standard_sub.lower():
                return standard_sub
    return None

def cor2suburb(coordinates):
    for ele in boundaryJS["features"]:
        if ele['geometry']['type']=='Polygon':
            if Polygon(ele["geometry"]["coordinates"][0]).contains(Point(coordinates)):
                return ele['properties']["SA2_NAME16"]
        elif ele['geometry']['type']=='MultiPolygon':
            for polygon in ele['geometry']['coordinates']:
                if Polygon(polygon[0]).contains(Point(coordinates)):
                    return ele['properties']["SA2_NAME16"]
    return None

def do100tweets(tweet_list):
    print(len(tweet_list))
    for tweet in tweet_list[1:]:
        tweetJS=tweet._json;
        if tweetJS["place"]:
            if tweetJS["place"]["place_type"]=="neighborhood":
                old_name = tweetJS["place"]["name"]
                new_name = sub_name_normalisation(old_name)
                if new_name !=None:
                    database.save({"suburb": new_name, "doc": tweetJS})
                    print(new_name)
                    continue
        if tweetJS["coordinates"]:
            long,lat = tweetJS["coordinates"]["coordinates"][0],tweetJS["coordinates"]["coordinates"][1]
            sub = cor2suburb([long,lat])
            if sub!=None:
                print([long, lat, sub])
                database.save({"suburb":sub,"doc":tweetJS})

# newer tweet has bigger id
# api.search(since_id, max_id=newest_id, count=min(100,count))
# return [maxID, down to about_count]
# or [max_id, down to the id just bigger than since_id]
# or [max_id, least_id within 10 days] when reaching the last-10-day limit
# each api can call search about 450 times within 15 mins, otherwise auto-wait least seconds until the next 15 mins
tweet_list =api_s[-1].search(geocode="-37.999250,144.997395,57km", count=100)
maxID = tweet_list[0].id
while len(tweet_list)>1:
    for api in api_s:
        tweet_list = api.search(max_id=maxID, geocode="-37.999250,144.997395,57km", count=100);
        try: do100tweets(tweet_list)
        except: pass
        maxID  = tweet_list[-1].id






