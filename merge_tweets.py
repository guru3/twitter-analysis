#!/usr/bin/env python
import os
import csv
import datetime

BASE_PATH = '.'
RAW_DATA_PATH = './raw_data'
MERGED_DIRECTORY = 'tweets_dirty'
DATETIME_FORMAT = "%Y_%m_%d_%H_%M_%S"

final_path = ''

def initialize():
	global final_path;
	final_path = os.path.join(BASE_PATH, MERGED_DIRECTORY)
	if( not os.path.exists( final_path ) ):
		os.mkdir( final_path );

def get_all_directories_time_sorted():
	l = os.listdir(RAW_DATA_PATH)
	all_timed_directories = [];
	for name in l :
		try:
			time = datetime.datetime.strptime(name, DATETIME_FORMAT) #format string shared with scrape_python. ideally should be at common place.
			all_timed_directories.append(time);
		except:
			print('Skipping name %s' % (name))

	all_timed_directories.sort()
	all_folders = [ datetime.datetime.strftime(x, DATETIME_FORMAT) for x in all_timed_directories];
	return all_folders;

def files_mapping():
	# for each twitter user to all its tweets
	sorted_directories = get_all_directories_time_sorted();
	file_to_paths = {};
	for directory in sorted_directories:
		dir_path = os.path.join(RAW_DATA_PATH, directory)
		files = os.listdir(dir_path)
		for file in files:
			if not( '.csv' in file ):
				continue;
			file_path = os.path.join(dir_path, file)
			try:
				file_to_paths[ file ].append( file_path );
			except:
				file_to_paths[ file ] = [ file_path ];
	return file_to_paths;

def merge_tweets():
	global final_path;
	user_to_tweet_files = files_mapping();
	for user in user_to_tweet_files:
		final_path_for_file = os.path.join(final_path, user);

		all_files = user_to_tweet_files[ user ];
		writer = csv.writer( open(final_path_for_file, 'w') );
		header_written = False;

		tweet_id_to_tweet = {};

		for file in all_files:
			header_expected = True;
			for line in csv.reader( open(file,'r') ):
				if header_expected:
					if not header_written:
						writer.writerow(line)
						header_written = True;
					header_expected = False;
					continue;
				#if we see the same tweet id again, we overwrite it
				#we receive directories in ascending order of time, so latest tweets will be seen later - so we get updated tweet information in merged data
				tweet_id_to_tweet[ int(line[0]) ] = line;
		
		all_tweet_ids = list(tweet_id_to_tweet.keys());
		all_tweet_ids.sort(reverse=True);
		for tweet_id in all_tweet_ids:
			writer.writerow( tweet_id_to_tweet[ tweet_id ] );

if __name__ == '__main__':
	initialize();
	merge_tweets();