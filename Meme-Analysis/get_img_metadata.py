# This script makes use of the ExifTool by Phil Harvey.
# Exiftool must be downloaded via the command line.
# This script creates a csv from a custom selection of metadata categories.

import os

#Step 1: Add directory for your images here
img_folder = "/Volumes/External_HD/Memes/Reddit/"

#Step 2: Make a selection of which metadata categories you will import into the new csv
os_command = "exiftool -csv -r -FileName -Subreddit -RedditUser -RedditPostDate -RedditPostTime -RedditScore -RedditNumCmts -TimeStamp -DeviceManufacturer -DeviceMfg -FileType -PrimaryPlatform -ProfileCopyright -Software -SlicesGroupName -MetadataDate -ModifyDate -Artist -CopyrightNotice -CreatorAddress -CreatorCity -CreatorCountry -CreatorPostalCode -CreatorRegion " + img_folder + " > Reddit_metadata.csv"
try:
    #twitter_command = "exiftool -csv -r -FileName -FileCreateDate -FileType -MetadataDate -ModifyDate -Artist -CopyrightNotice -CreatorAddress -CreatorCity -CreatorCountry -CreatorPostalCode -CreatorRegion -FileAttributes -FileSize -MDItemContentType -JPEGQualityEstimate -ProcessingTime " + img_folder + " > all_crowdtangle_metadata.csv"
    print("Beginning extraction...")
    os.system(os_command)
    print("Finished extraction")
except Exception as ex:
    print("Unix command unsuccessful.")