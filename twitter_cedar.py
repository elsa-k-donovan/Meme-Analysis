import zipfile
import os
import csv
import pandas as pd
import shutil
import glob
import ntpath

###########################################################################
# Change all of the paths and variables in this section
# for batch processing on Cedar.

root_path = "Volumes/Elsa_HD2/Memes/"

# path to zip file
path_zip = "/Volumes/Elsa_HD2/Memes/fb_test.zip"
path_zip_dest = "/Volumes/Elsa_HD2/Memes/Twitter/Results"

# path to csv
path_csv = "/Volumes/Elsa_HD2/Memes/Twitter/twitter_filenames.csv"

name_of_zip = "fb_test"

imgs_per_extraction = 100,000
max_imgs_per_folder = 100,000

###########################################################################


# file formats that we expects to see in zip
FileFormats = ['.jpg', '.png', '.gif']


counter = 0
files_moved_count = 0
folder_num = 1

def checkCsv(name):

    df = pd.read_csv(path_csv)

    name = ntpath.basename(name)
    print("Filename still is " + name)
    name_col = df.filename
    cols = pd.Series(name_col)

    if name in cols.values:
        print("Found image that matches a filename in the csv...")
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
        if "/." not in item and not item.endswith("/"):
            listOfFileNames.append(item)

    for i in listOfFileNames:
        print(i)

    for k in range(0, len(listOfFileNames), imgs_per_extraction):
        print("Beginning extraction of all files in zip...")
        print("Value of k: " + str(k))

        print("Number of total files: " + str(len(listOfFileNames)))
        x = k

        zip_ref.extractall(members=listOfFileNames[k:k + imgs_per_extraction], path=path_zip_dest)


        try:
            num_loops = x + 20
            #x = 0
            while x < num_loops:

                path_of_file = listOfFileNames[x]
                print("Value of x: " + str(x))

                #head, file_name = os.path.split(path_of_file)
                print("File name is: " + path_of_file)

                if(checkCsv(path_of_file)):
                    print("Writing to new folder...")
                    print(path_zip_dest + "/" + path_of_file)

                    # create new folder
                    if files_moved_count >= max_imgs_per_folder or folder_num == 1:

                        dest_dir_path = path_zip_dest + "/folder_" + str(folder_num)
                        print(dest_dir_path)

                        if not os.path.exists(dest_dir_path):
                            print("Creating new folder at " + dest_dir_path)
                            folder_num += 1
                            files_moved_count = 0
                            os.makedirs(dest_dir_path)

                    cmd = "cp " + path_zip_dest + "/" + path_of_file + " " + dest_dir_path
                    os.system(cmd)
                    files_moved_count += 1
                    print("Files moved to folder: " + str(files_moved_count))

                counter += 1
                x+=1
        except Exception as ex:
            print("out of range")

        print("There are " + str(counter) + " files.")
        print(str(folder_num) + " new folders have been created.")

        print("Removing files extracted in test folder.")

        cmd_rm = path_zip_dest + "/" + name_of_zip
        try:
            shutil.rmtree(cmd_rm)
        except OSError as e:
            print("Error: %s : %s" % (cmd_rm, e.strerror))

