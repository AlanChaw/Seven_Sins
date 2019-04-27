# # get tweepy api object
# import tweepy
# consumer_key = 'v0972w9aptiA8Dzm97sGFykPY'
# consumer_secret = 'e9P4IMHyWEIwqwKiYVu4qDwXLMBooockFeqs5lwkjhCvJ0efle'
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
# # access_key = '988266868828815360-LUDs2XCggWF57JVCZpOSvDTyxYNxEcg'
# # access_secret = 'GdkzCMPkAFhJU6jHfr15ZD4TmSETTW41RQLxp3lNODoVL'
# # auth.set_access_token(access_key, access_secret)
# # api = tweepy.API(auth)

# # connect to database
# import couchdb
# couch = couchdb.Server("http://115.146.92.183:5984")
# database = couch['jan_to_apr_by_region']
# database.save({"a": 123})


# # get google map api object
# import googlemaps
# gmaps = googlemaps.Client(key='AIzaSyBJSHURhn2lPbsK8P1A1TK17XZvC_zTdCg')
# print (gmaps.reverse_geocode((-37.81194167,144.95)))


# api.search(q="haha", count=5, since_id=12345, max_id=54321)
# search()[k].id  ==  search()[k]._json["id"] == 该推文的唯一id == 可进行since_id与max_id的比较
# 从max_id往下走(时间变早, 往前回溯), 直到看到since_id或达到大约的count数量, 返回[since_id后一个,max_id]的tweetObjList
# 每个15分钟内可call search()大约450次, 达到则自动卡最短时间直到下个时间段, 每次返回大约的min(count,100)的tweets,
# q 为精确查找还是模糊查找?


# c = tweepy.Cursor(api.search,q="haha").items()
# iteration=0;error=0;place=0;coor=0;
# file2 = open(r"result.txt","w+")
# while True:
#     if iteration==25000:break
#     try:
#         tweet = c.next()._json
#         if tweet["coordinates"]!= None or tweet["place"]!= None:
#             if tweet["coordinates"]!=None: coor+=1
#             if tweet["place"]!=None:place+=1
#             file2.write(json.dumps({"coor":tweet["coordinates"],"place":tweet["place"],"time":tweet["created_at"]}));file2.write("\n")
#         iteration+=1;print(iteration)
#     except tweepy.TweepError:print("too many requests, sleep 60 seconds");time.sleep(60)
#     except StopIteration:print("break from stop"); break
#     except:error+=1;
# print ([iteration,error,place,coor])


# # to save raw data
# import json
# import couchdb
# couch = couchdb.Server("http://115.146.92.183:5984")
# fileR = open('raw2018monthMel.json', 'rb')
# i=0;jump=0;newLine = fileR.readline()
# while newLine:
#     i += 1;print (i)
#     try:
#         newLine = fileR.readline()
#         tweetJS = json.loads(newLine.decode().strip().strip(','))
#         if tweetJS["doc"]["coordinates"]:couch['month_by_coor'].save({"doc": tweetJS})
#         elif tweetJS["doc"]["place"]:
#             if tweetJS["doc"]["place"]["place_type"]=="poi": couch['month_by_coor'].save({"doc": tweetJS})
#             elif tweetJS["doc"]["place"]["place_type"]=="neighborhood": couch['month_by_region'].save({"doc": tweetJS})
#             elif tweetJS["doc"]["place"]["place_type"]=="city": couch['month_by_city'].save({"doc": tweetJS})
#     except:jump+=1
# print([i,jump])


# to save cleaned data
import json
import couchdb
couch = couchdb.Server("http://115.146.92.183:5984")
database = couch['mar_by_region']
fileR = open('nei2018marMel.json', 'rb')
newLine = fileR.readline()
while newLine:
    database.save({"doc": json.loads(newLine)})
    newLine = fileR.readline()






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





