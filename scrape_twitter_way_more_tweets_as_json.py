#!/usr/bin/env python

# Do download twint to be able to use it
import csv
import sys
import time
import os
import datetime
import json

RAW_DATA_PATH = './raw_data/'
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def get_until_tweet( user ):
    input_file = os.path.join(RAW_DATA_PATH + 'partial/', user+ '_tweets.json')
    if not os.path.exists( input_file ):
        return None

    last_row = None
    with open( input_file, "r") as read_file:
        for line in read_file.readlines():
            data = json.loads(line)
            last_row = data

    date = last_row["date"]
    dt = datetime.datetime.strptime(last_row["date"] + ' ' + last_row["time"], DATETIME_FORMAT)
    dt = dt + datetime.timedelta(days=1)
    get_until = dt.strftime(DATETIME_FORMAT)
    return get_until

def get_all_tweets(screen_name):
    get_until = get_until_tweet(screen_name)
    # output_file_name = path + '/%s_tweets.csv' % screen_name;
    output_file_name = RAW_DATA_PATH + '/%s_tweets.json' % screen_name;
    # command = 'twint -u %s --since "2019-01-01 00:00:00" -o %s --csv > /dev/null' % (screen_name, output_file_name)
    if get_until == None:
        command = 'twint -u %s --since "2018-12-31 00:00:00" -o %s --json > /dev/null' % (screen_name, output_file_name)
    else:
        command = 'twint -u %s --since "2018-12-31 00:00:00" --until "%s" -o %s --json > /dev/null' % (screen_name, get_until, output_file_name)
    print(command)
    os.system(command)

def exists(screen_name):
    filename = RAW_DATA_PATH + '/json_since_2019/' + screen_name +'_tweets.json'
    return os.path.exists(filename)

def merge_tweet(screen_name):
    input_file_name = RAW_DATA_PATH + '/%s_tweets.json' % screen_name;
    final_file_name = RAW_DATA_PATH + '/partial/%s_tweets.json' % screen_name;
    
    all_data = {}
    if os.path.exists(input_file_name):
        for line in open( input_file_name, 'r' ).readlines():
            data = json.loads(line)
            id_ = int(data['id'])
            all_data[id_] = line

    if os.path.exists(final_file_name):
        for line in open( final_file_name, 'r' ).readlines():
            data = json.loads(line)
            id_ = int(data['id'])
            all_data[id_] = line

    ids = list(all_data.keys())
    ids.sort(reverse=True)
    lines = [ all_data[i] for i in ids ]

    last_line = lines[-1]
    last_row = json.loads(last_line)
    dt = datetime.datetime.strptime(last_row["date"] + ' ' + last_row["time"], DATETIME_FORMAT)
    if( dt.year == 2018 ):
        file = open( RAW_DATA_PATH + '/json_since_2019/' + screen_name +'_tweets.json', 'w' )
        file.writelines(lines)
        os.system('rm %s' % input_file_name)
        os.system('rm %s' % final_file_name)
    else:
        file = open( final_file_name, 'w' )
        file.writelines(lines)
        os.system('rm %s' % input_file_name)

if __name__ == '__main__':
    #pass in the username of the account you want to download
    users = [
     'republic',
     'ndtvfeed',
     'ZeeNewsEnglish', 
     'PTI_News', 'TimesNow', 
     'timesofindia', 'IndianExpress', 'TOIIndiaNews',

    # 'ThePrintIndia', 'the_hindu', 'thewire_in', 
    # 'narendramodi', 'ArvindKejriwal', 'realDonaldTrump', 
    ]
    for i in range(100):  #it fails intermittently sometimes
        for name in users:
            if exists(name):
                continue
            print('\nGetting tweets for %s' % name)
            try:
                get_all_tweets( name )
            except:
                print('Failed intermittently')
            merge_tweet(name)

