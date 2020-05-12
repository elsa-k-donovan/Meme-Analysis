import pandas as pd
import requests
import os.path
import re


#location of tsv or csv to be read
path = 'links.tsv'
print('opened file')

#col_list to be replaced by named of the columns to show
#col_list = ["URL","HTTP","Signed URL"]


#use pandas read_csv, only read Signed URl col
df = pd.read_csv(path, delimiter="\t", usecols=["Signed URL"], encoding="utf-16")

#file path to where the downloaded file should go
finalSavePath = '/.../'


for i in range(len(df)):
    strURLs = df.loc[i, "Signed URL"]
    print(strURLs)

    zipurl = strURLs
    resp = requests.get(zipurl)

    #find file name in url
    zname = re.search('ddp-images/(.*)\?x-goog-signature', zipurl)
    finalName = zname.group(1)

    print(finalName)

    completeName = os.path.join(finalSavePath, finalName)
    saveFile = open(completeName, 'wb')

    saveFile.write(resp.content)
    saveFile.close()

