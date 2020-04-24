import csv
import re
import os
import string
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from nltk.stem import WordNetLemmatizer 
from nltk.tokenize import word_tokenize

BASE_PATH = '.'
DIRTY_DIRECTORY = 'tweets_dirty'
CLEAN_DIRECTORY = 'tweets'
DATETIME_FORMAT = "%Y_%m_%d_%H_%M_%S"

final_path = ''

lemmatizer = WordNetLemmatizer() 

def initialize():
	global final_path;
	final_path = os.path.join(BASE_PATH, CLEAN_DIRECTORY)
	if( not os.path.exists( final_path ) ):
		os.mkdir( final_path );

def clean_text( text ):
	global lemmatizer
	isOriginalNearLimit = len(text) > 130

	#first for very clumsy rules
	for char in [ '"', "'" ]:
		if text[0:2] == 'b' + char:
			text = text[2:]
		text = text.replace(char,'')

	strings_to_replace = [
		[ 'https://t.co/', 23 ],
		[ 'http://t.co/', 22 ],
		[ '\\x', 4 ] ]            #text = re.sub(r'[^\x00-\x7F]+',' ', text)
	for [ word, length ] in strings_to_replace:
		indices = [n for n in range(len(text)) if text.find(word, n) == n]
		removed = 0;
		for i in indices:
			i = i - length*removed
			text = text[:i] + text[i+length:]
			removed = removed + 1

	# remove special character
	table = str.maketrans('', '', string.punctuation)
	text = text.translate(table)

	# no digits
	text = re.sub(r'\d+', '', text)

	# to lower
	text = text.lower()
	
	# no stopwords
	text_subsets = word_tokenize(text)
	text_subsets = [w for w in text_subsets if not w in ENGLISH_STOP_WORDS]

	text_new_subsets = [];
	for char in text_subsets:
		#personal decision to remove characters less than size 3
		if len(char) < 3:
			continue;
		text_new_subsets.append(lemmatizer.lemmatize(char))
	
	#if we miss anything non-alphabetic, let's remove it here
	text_new_subsets = [ x for x in text_new_subsets if x.isalpha()  ]
	if isOriginalNearLimit:
		#tweet is not complete, so we omit last word in case it is partial
		text_new_subsets = text_new_subsets[:-1]
	text = " ".join(text_new_subsets) 
	return text

def clean_data( input_file, output_file ):
	reader = csv.reader( open(input_file, 'r') )
	writer = csv.writer( open(output_file, 'w') )
	for row in reader:
		row[2] = clean_text( row[2] )
		if len( row[2] ) == 0:
			#skip empty tweets
			continue; 
		writer.writerow(row)

if 	__name__ == "__main__":
	initialize()
	dirty = os.path.join(BASE_PATH, DIRTY_DIRECTORY)
	list_dirty_files = os.listdir(dirty)
	for file in list_dirty_files:
		input_file = os.path.join(dirty, file)
		output_file = os.path.join(final_path, file)
		clean_data(input_file, output_file)