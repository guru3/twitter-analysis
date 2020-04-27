#!/usr/bin/env python

# Do download twint to be able to use it
import csv
import sys
import time
import os
import datetime
import json
import re
import string
from mtranslate import core
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from nltk.stem import WordNetLemmatizer 
from nltk.tokenize import word_tokenize

RAW_FILE_PATH = './raw_data/json_since_2019/'
FINAL_PATH = './clean_data/'

lemmatizer = WordNetLemmatizer() 

def initial_clean_up( text ):
	# 0. remove hyperlinks
	text_split = filter(lambda x: x[0:4]!='http' and x[0:15]!= 'pic.twitter.com', text.split())
	text = ' '.join(text_split)

	# 1. replace \n , .
	for char in ['\n','.',',','…','-',':',';']:
		text = text.replace(char, ' ')
	for char in ["'",'"','’']:
		text = text.replace(char, '')

	# remove emoji
	emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
	text = emoji_pattern.sub(r'', text) # no emoji

	# only utf-8
	text = text.encode("utf-8").decode("utf-8",'ignore')
	return text

def translate(text):
	if( sum( [ ord(i)//128 for i in text ] ) ):
		#translate only if needed
		text = core.translate(text, to_language='en')
	return text

def clean_text( text ):
	global lemmatizer

	text = initial_clean_up(text)
	# isOriginalNearLimit = len(text) > 130

	# remove special character
	table = str.maketrans('', '', string.punctuation)
	text = text.translate(table)

	# no digits
	text = re.sub(r'\d+', '', text)
	
	text = translate(text);

	# to lower
	text = text.lower()
	
	# # no stopwords
	text_subsets = word_tokenize(text)
	text_subsets = [w for w in text_subsets if not w in ENGLISH_STOP_WORDS]

	text_new_subsets = [];
	for char in text_subsets:
		if len(char) < 3: #any word less than or equal to 2
			continue
		text_new_subsets.append(lemmatizer.lemmatize(char))
	
	#if we miss anything non-alphabetic, let's remove it here
	text_new_subsets = [ x for x in text_new_subsets if x.isalpha()  ]
	
	text = " ".join(text_new_subsets) 
	return text


def clean_tweets( user ):
	rLines = [];
	final_file = os.path.join(FINAL_PATH, user+ '_tweets.json')
	if os.path.exists(final_file):
		with open( final_file, 'r' ) as r:
			for l in r.readlines():
				rLines.append(l)

	input_file = os.path.join(RAW_FILE_PATH, user+ '_tweets.json')
	outputs = [];
	output_file = open( final_file, 'w' )
	with open( input_file, "r", encoding='utf8', errors='ignore') as read_file:
		intermediary_jsons = [];
		intermediary_texts = [];
		i = 0
		for line in read_file.readlines():
			if i < len(rLines):
				line = rLines[i]
				output_file.write(line)
			else:
				data = json.loads(line)
				data["tweet"] = clean_text( data["tweet"] )
				line = json.dumps(data)
				output_file.write(line + os.linesep)
			i = i + 1
			
if __name__ == '__main__':
	users = [ 'IndianExpress', 'timesofindia',  'TOIIndiaNews', 'ThePrintIndia', 'the_hindu', 'thewire_in' ]
	for user in users:
		print('Cleaning tweets for ', user)
		clean_tweets(user)
