import csv
import os
import json

JSON_PATH = './clean_data'
CSV_PATH = './tweet_data'

def get_csv_row( json ):
	id_ = json["id"]
	epoch = json["created_at"]//1000  #to change to timestamp, datetime.datetime.fromtimestamp()
	tweet = json["tweet"]
	assert( not ',' in tweet )
	mentions = '@'.join(json["mentions"])
	replies_count = json["replies_count"]
	retweets_count = json["retweets_count"]
	likes_count = json["likes_count"]
	hashtags = "#".join( json["hashtags"] )

	return([id_, epoch, tweet, mentions, replies_count, retweets_count, likes_count, hashtags ])

def create_csv_from_json( file ):
	json_file = os.path.join(JSON_PATH, file)
	filename = file[:-4] + 'csv'
	csv_writer = csv.writer( open( os.path.join(CSV_PATH, filename), 'w') )
	csv_writer.writerow(['id','epoch', 'tweet','mentions','replies_count','retweets_count','likes_count','hashtags'])
	with open(json_file, 'r') as file:
		for line in file.readlines():
			data = json.loads(line)
			data = get_csv_row(data)
			csv_writer.writerow(data)
			

if __name__ == "__main__":
	files = os.listdir(JSON_PATH)
	for file in files:
		if file.endswith('.json'):
			create_csv_from_json(file)