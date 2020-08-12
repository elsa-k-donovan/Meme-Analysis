from datetime import datetime
from psaw import PushshiftAPI
import wget
import os

# Easy conversion for date to UNIX timestamps here: https://www.unixtimestamp.com/index.php

# pushshift.io API
api = PushshiftAPI()

local_path = os.getcwd()

curr_date = str(datetime.date(datetime.now()))
curr_date = curr_date.replace('-','')

#Add subreddits
sub_list = ['subreddit1', 'subreddit2']

#Add timeframe
after = "1567296000" #Sept 1, 2019
before = '1575158340' #Nov 30, 2019

for subreddit in sub_list:
    print("Scraping images in "+str(subreddit)+" begins...")
    print("...")

    meme_list = list(api.search_submissions(subreddit=str(subreddit), filter=['url'], after=str(after), before=str(before)))

    #create folders for each subreddit
    day_dir = local_path + "/files/"+str(subreddit)+"/" + curr_date + "/"

    try:
        os.mkdir(day_dir)
    except OSError:
        print ("Creation of the directory %s failed" % day_dir)
    else:
        print ("Successfully created the day directory %s " % day_dir)

    counter = 0

    for meme in meme_list:
        #scrapes jpg, gif, and png
        if (str(meme.url).endswith('.jpg') or str(meme.url).endswith('.gif') or str(meme.url).endswith('.png')) and not str(meme.url).startswith('https://i.imgflip.com'):
            print(meme.url)

            try:
                file_name = wget.download(meme.url,day_dir)
                counter += 1
            except Exception as ex:
                print("URL not found")

    print(str(counter)+" images from "+str(subreddit)+" successfully downloaded.")
    print("...")

