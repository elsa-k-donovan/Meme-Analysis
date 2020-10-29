#4Plebs API Documentation found here: https://4plebs.tech/foolfuuka/#4plebs-specific-boards-information

import os
import wget
import urllib.request
import json
import requests
import pandas as pd
import csv
import time

# CHANGE THESE SETTINGS!
saveDirectory = "C:/Users/elsa/Downloads/4chan_scrape"


counter = 0
total_posts = 0

#PARAMETERS
start = "2019-10-14" #Sept 1, 2019
end = '2019-10-21' #Nov 30, 2019
board_url = 'pol'
country_code = 'CA'

current_page = 0

print("The current working directory is " + saveDirectory)

# First we'll try to create a folder for the board.
path = saveDirectory + "/" + board_url

try:
    os.mkdir(path)
except OSError:
    print("Creation of the directory %s failed  - possible directory already exists" % path)
else:
    print("Successfully created the directory %s" % path)


# Get the 4chan board catalog JSON file and open it
base_url = "https://archive.4plebs.org/_/api/chan/search/?boards="+ board_url + "&start="+ start +"&end=" + end + "&country=" + country_code + "&page=" + str(current_page)
print(base_url)

#+ str(current_page)
result = requests.get(base_url)
result.raise_for_status()
print(result.text)
result = json.loads(result.text)["0"]["posts"]

pd_result = pd.json_normalize(result)
df = pd.DataFrame(pd_result)
print(df)

while current_page != None:

    base_url = "https://archive.4plebs.org/_/api/chan/search/?boards=" + board_url + "&start=" + start + "&end=" + end + "&country=" + country_code + "&page=" + str(current_page)
    print(base_url)
    time.sleep(20)

    result = requests.get(base_url)
    result.raise_for_status()
    result = json.loads(result.text)["0"]["posts"]

    pd_result = pd.json_normalize(result)
    df = pd.DataFrame(pd_result)

    for i in range(0, len(df)):
        total_posts += 1
        try:
            image_url = df['media.media_link'][i]
            print(image_url)
        except Exception as ex_media:
            print("No media.media_link.")



        try:
            file_name = wget.download(image_url, path)
            counter += 1

            try:
                name = df['name'][i]
                timestamp = df['timestamp'][i]
                date = df['fourchan_date'][i]
                country = df['poster_country_name'][i]

                filename = df['media.media'][i]
                board = df['board.name'][i]
                board_shrt = df['board.shortname'][i]

                with open('4chan-metadata.csv', 'a+', newline='') as csv_file:
                    spamwriter = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    spamwriter.writerow([image_url, filename, board, board_shrt, name, timestamp, date, country])

            except Exception as ex1:
                print("Could not retrieve info.")

        except Exception as ex:
            print("URL not found")

        print(str(counter) + " images successfully downloaded from page " + str(current_page) + ".")
        print("...")
        print("Total posts searched: " + str(total_posts))

    current_page += 1

print("Total posts searched: " + str(total_posts))
print("Script completed")

