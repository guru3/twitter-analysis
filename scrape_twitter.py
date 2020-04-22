#!/usr/bin/env python
import tweepy
import csv
import sys
import time
import os
import datetime

RAW_DATA_PATH = './raw'
DATETIME_FORMAT = "%Y_%m_%d_%H_%M_%S"

consumer_key = '';
consumer_secret = ''
access_key = ''
access_secret = ''
path = ''

def initializeKeys():
	global consumer_key, consumer_secret, access_key, access_secret;
	local_map = {}
	for line in csv.reader( open('./twitterapi.key','r') ):
		local_map[line[0]] = line[1];
	consumer_key = local_map['consumer_key'];
	consumer_secret = local_map['consumer_secret'];
	access_key = local_map['access_key'];
	access_secret = local_map['access_secret'];
  
def initialize():
	global path
	initializeKeys();
	time = datetime.datetime.now().strftime(DATETIME_FORMAT)
	path = os.path.join(RAW_DATA_PATH, time);
	if( not os.path.exists(path) ): #it should never be, but doesn't hurt to check
		os.mkdir(path);

def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	try:
		new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	except:
		new_tweet = []

	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		try:
			new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		except:
			new_tweets = []

		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print( "...%s tweets downloaded so far" % (len(alltweets)) )

	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), 
	tweet.in_reply_to_user_id_str, tweet.in_reply_to_screen_name, tweet.retweet_count, 
	tweet.favorite_count, tweet.favorited, tweet.retweeted, tweet.is_quote_status ] for tweet in alltweets]

	#write the csv	
	with open(path + '/%s_tweets.csv' % screen_name, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text", "in_reply_to_user_id", "in_reply_to_screen_name", 
			"retweet_count", "favorite_count" ,"favorited", "retweeted", "is_quote_status"])
		writer.writerows(outtweets)


if __name__ == '__main__':
	initialize();
	#pass in the username of the account you want to download
	users = ['timesofindia', 'republic', 'thewire_in', 'ndtvfeed', 'ZeeNewsEnglish', 
	'PTI_News', 'ABPNews', 'TimesNow', 'News18India', 'IndianExpress', 'TOIIndiaNews',
	'ThePrintIndia', 'the_hindu',
	
	'realDonaldTrump', 

	'narendramodi', 'ArvindKejriwal',

	'iamsrk', 'aamir_khan', 'priyankachopra', 'SrBachchan', 'BeingSalmanKhan', 'iamsrk', 
	'akshaykumar', 'deepikapadukone', 'iHritik', 'juniorBachchan',
	'sonamakapoor', 'karanjohar', 'shahidkapoor', 'FarOutAkhtar', 'aliaa08',
	'AnushkaSharma', 'sonakshisinha', 'iamVkohli', 'sachin_rt', 
	]
	
	for name in users:
		print('\nGetting tweets for %s' % name)
		get_all_tweets( name )
		time.sleep(5)