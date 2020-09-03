import zipfile
import os
import csv
import pandas as pd
import glob

# The goal of this code is to demonstrate how to incrementally move and remove files from a zipfile
# This is an example of how we can handle files in cedar as there is a 1M file limit
# It is recommended to use absolute paths

root_path = "Volumes/Elsa_HD2/Memes/"

# file formats that we expects to see in zip
FileFormats = ['.jpg', '.png', '.gif']

# path to zip file
path_zip = "/Volumes/Elsa_HD2/Memes/fb_test.zip"
path_zip_dest = "/Volumes/Elsa_HD2/Memes/Twitter/Results"

# path to csv
path_csv = "/Volumes/Elsa_HD2/Memes/Twitter/twitter_filenames.csv"


def checkCsv(name):
    print("Check csv function called.")

    df = pd.read_csv(path_csv)
    print(name)
    name_col = df.filename

    # scan through entire csv document to see if it is in column[5]
    if (name in name_col):
        return True
    else:
        return False




# Lets open the zipfile so we can process
with zipfile.ZipFile(path_zip, 'r') as zip_ref:
    # lets get a list of all files in zip
    print("Getting List of all the File Names...")
    listOfFileNames_temp = zip_ref.namelist()
    listOfFileNames = []

    # lets remove the non file paths
    for item in listOfFileNames_temp:
        for format_i in FileFormats:
            if format_i in item:
                print("Removed non file paths...")
                listOfFileNames.append(item)

    # now all we need to do is extract using the list!
    # this will do increments of 500
    for k in range(0, len(listOfFileNames), 500):
        print("Beginning extraction of 500 files in zip...")

        zip_ref.extractall(members=listOfFileNames[k:k + 500], path=path_zip_dest)

        counter = 0
        try:
            for x in range(0, 500):
                if (x % 2 == 0):
                    path_of_file = listOfFileNames[x]
                    head, file_name = os.path.split(path_of_file)
                    print(file_name)

                    #TODO: This is the part that needs to be finished.
                    # if checkCSV returns true then make a copy of image inside of a new folder.
                    if(checkCsv(file_name)):
                        print("Writing to new folder...")
                        #copy each chunk of 500 images to new folders




                    counter += 1
        except Exception as ex:
            print("out of range")

        print("There are " + str(counter) + " files.")

        os.system("rm -rfv data/*")
