
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, json
import sys
import datetime
import urllib, json

def timeStamped(fname, fmt='{fname}_%Y-%m-%d-%H-%M-%S'):
    return datetime.datetime.now().strftime(fmt).format(fname=fname)

def recursive_ascii_encode(lst):
    ret = []
    for x in lst:
        if isinstance(x, basestring):  # covers both str and unicode
            ret.append(x.encode('ascii', 'ignore'))
        else:
            ret.append(recursive_ascii_encode(x))
    return ret



CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

world_woeid = 1
us_woeid = 23424977

#world_trends = api.trends_place(world_woeid) 
#us_trends = api.trends_place(us_woeid)
# print trends1
#world_trends_set = set([trend['name'] for trend in world_trends[0]['trends']])
#us_trends_set = set([trend['name'] for trend in us_trends[0]['trends']])
#common_trends = world_trends_set.intersection(us_trends_set)

#hashtags = [trend['name'] for trend in us_trends[0]['trends'] if trend['name'].startswith('#')]



#lets call this api now http://api.whatthetrend.com/#trends.v2
url = "http://api.whatthetrend.com/api/v2/trends.json"
response = urllib.urlopen(url);
data = json.loads(response.read())

trending = set([trend['name'] for trend in data['trends']])

#for hashtag in hashtags:
#  print(hashtag)

i=0
res = ''
# get google trends
# url = "http://hawttrends.appspot.com/api/terms/"
url = "http://www.google.com/trends/api/stories/summary?id=US_lnk_vc1XjgAwAADq8M_en&id=US_lnk_izkijgAwAACpBM_en&id=US_lnk_9t9SjgAwAACk4M_en&id=US_lnk__JBQjgAwAACsrM_en&id=US_lnk_em5PjgAwAAA1UM_en&id=US_lnk_C9hdjgAwAABW5M_en&id=US_lnk_-yJCjgAwAAC5HM_en&id=US_lnk_v4BBjgAwAAD-vM_en&id=US_lnk_roZdjgAwAADzuM_en&id=US_lnk_xyVbjgAwAACcGM_en&id=US_lnk_YwtZjgAwAAA6NM_en&id=US_lnk_rCBajgAwAAD2HM_en&id=US_lnk_wbxcjgAwAACdgM_en&id=US_lnk_2WdYjgAwAACBWM_en&id=US_lnk_EYBTjgAwAABCvM_en&tz=420"
url = "http://www.google.com/trends/api/stories/latest?cat=all&fi=9&fs=9&geo=US&ri=300&rs=15&tz=420"

response = urllib.urlopen(url);

data = json.loads(response.read()[5:])
google_set = data["trendingStoryIds"]

# i know the legth of google_set
item_count = len(google_set)
print "================="
print item_count
print '\\n'
print google_set[1]
print "================="

results = []

x=0
while x < item_count:  
  while i < 150: 
    print x
    res = res + "&id=" + google_set[x]
    i+=1
    x+=1

  res = res[1:]
  url = "http://www.google.com/trends/api/stories/summary?"+res+"&tz=420"
  print url + '\\n'
  # now fetch the chunk of data
  response = urllib.urlopen(url);
  data = json.loads(response.read()[5:])
  # store the results
  google_trending_set = list([trend['entityNames'] for trend in data['trendingStories']])

  results += google_trending_set
  i=0
  res=''

#response = urllib.urlopen(url);

#data = json.loads(response.read()[5:])

#print data

# google_trending_set = list([trend['entityNames'] for trend in data['trendingStories']])

# print google_trending_set

#google_trending_set = data['trendingStories']['entityNames']



#print "US trends\n", us_trends_set, "\n"
#print "Common trends\n", common_trends, "\n"
#print "WhatTheTrend\n", trending, "\n"
print "Google US Trends\n", google_trending_set, "\n"


#backup = sys.stdout
#sys.stdout = StringIO()
#out = us_trends_set
#sys.stdout.close()
#sys.stdout = backup

#filename = '/home/mishab/Twitter/twitter-trends-%s.txt'%datetime.now().strftime('%Y-%m-%d')
filename = '/home/mishab/google/twitter-trends-txt'

with open(timeStamped(filename),'w') as outf:
  #for item in us_trends_set:
  #  outf.write("%s\n" % item.encode('utf-8'))
  #outf.write("=\n")
  #for item in trending:
  #  outf.write("%s\n" % item.encode('utf-8'))
  #outf.write("=\n")
  for item in results:
    outf.write("%s\n" % '|'.join(recursive_ascii_encode(item)))
  #  outf.write("%s\n" % item.encode('utf-8'))


outf.close()

#f = open(filename,'w')
#f.close()
