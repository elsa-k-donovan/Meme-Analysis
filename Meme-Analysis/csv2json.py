import json
import pandas as pd

# Step 1: Change the following to the appropriate file paths.

# Change these file paths to your specific files.
CsvFile = 'bin/memes_beta_metadata.csv'

# This file is the one created by feature extraction scripts.
JsonFile = 'bin/memes-beta-features.json'

# This is a separate file that was created using feature extractions.
#append_JsonFile = 'july13-points-facebook.json'

counter = 0
i = 0
j = 0

js_df = pd.read_json(JsonFile)

df = pd.read_csv(CsvFile)

#a_js_df = pd.read_json(append_JsonFile)

output = []

for i in range(len(js_df['path'])):
    for j in range(len(df['SourceFile'])):

        if js_df['path'].iloc[i] == df['SourceFile'].iloc[j]:
            print("Found Match")


            filename = str(df['FileName'].iloc[j])
            subreddit = str(df['Subreddit'].iloc[j])
            redditUser = str(df['RedditUser'].iloc[j])
            redditDate = str(df['RedditPostDate'].iloc[j])
            redditTime = str(df['RedditPostTime'].iloc[j])
            socialmedia = str(df['SocialMedia'].iloc[j])
            point = js_df['point'].iloc[i]

            try:
                int_timestamp = int(df['TimeStamp'].iloc[j])
                timestamp = str(int_timestamp)
                print("TimeStamp: " + timestamp)
            except Exception as notFound:
                print("TimeStamp information not found.")

            filepath = js_df['path'].iloc[i]

            print(filename)
            print("JSON filepath: " + filepath)
            print("Subreddit: " + subreddit)
            print("RedditUser: " + redditUser)
            print("File Name: " + filename)
            # print("Point: " + point)
            print()

            #json_row = str(js_df.iloc[i].to_json())
            json_row = {"path": filename}
            z = json_row

            print(json_row)

            # Step 2: This is a custom variable. You must set it based on your knowledge of the dataset.
            #socialmedia = "reddit"

            # Adding metadata categories to new JSON file
            # new point adds extra digits
            y = {"point": point, "socialmedia": socialmedia, "subreddit": subreddit, "redditUser": redditUser, "postDate": redditDate, "postTime": redditTime}

            #z = json.loads(json_row)

            z.update(y)
            # z.update(comma)
            print(z)

            print("...")
            print()
            print("...")

            output.append(z)

            counter+=1
        #else:
            #print("no match")
print(counter)

# for i in range(len(a_js_df['path'])):
#     json_row = str(a_js_df.iloc[i].to_json())
#
#     z = json.loads(json_row)
#
#     # This is a custom variable. You must set it based on your knowledge of the dataset.
#     socialmedia = "facebook"
#     blank = "null"
#
#     y = {"socialmedia": socialmedia, "postDate": blank, "subreddit": socialmedia}
#
#     z.update(y)
#
#     print(z)
#
#     print("...")
#     print()
#     print("...")
#
#     output.append(z)
#
#     counter += 1
#     # else:
#     # print("no match")
# print(counter)


# merge both json files into new json file
# write to brand new file
with open('memes_viewer_data.json', 'w') as f:
    json.dump(output, f)
