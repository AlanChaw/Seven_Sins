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

def do1tweet(json_tweet):
    print(json_tweet)
    if json_tweet["place"]:
        if json_tweet["place"]["place_type"]=="neighborhood":
            old_name = json_tweet["place"]["name"]
            new_name = sub_name_normalisation(old_name)
            if new_name !=None:
                database.save({"suburb": new_name, "doc": json_tweet})
                print(new_name)
                return True
    if json_tweet["coordinates"]:
        long,lat = json_tweet["coordinates"]["coordinates"][0],json_tweet["coordinates"]["coordinates"][1]
        sub = cor2suburb([long,lat])
        if sub!=None:
            database.save({"suburb":sub,"doc":json_tweet})
            print([long, lat, sub])
            return True
    return False

class MyStreamListener(tweepy.StreamListener):
    i = 0
    def on_data(self, data):
        jsontweet=json.loads(data);
        try:
            bool = do1tweet(jsontweet)
            if bool == True: self.i += 1
        except:pass
        if self.i>=5000:return False

auth= tweepy.OAuthHandler('rcFJ0DzhHSDvTfgHK49WMCc9S', 'LZdhAUDVvnWcHHxUXTzYQF2f57KrNfmtEZHCmKzNZjxxsuG0Bp')
auth.set_access_token('1121779286069760000-UHzlxp96uTyQXjtHJFm5rLqzI0TRuH', 'yHrsQCrFWzlHhSyoPetkRW0ACNu4mzpSq1YRPkdZzgaFL')
myStream = tweepy.Stream(auth = auth, listener=MyStreamListener())
myStream.filter(locations=[144.293405,-38.548275,145.493112,-37.505479])