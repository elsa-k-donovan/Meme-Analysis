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

#root_path = "/home/edonovan/projects/def-whkchun/memes/images/CA_2019Elections/twitter"

# path to zip file
path_zip = "/home/edonovan/projects/def-whkchun/memes/images/CA_2019Elections/twitter/twitter_fixed.zip"

path_zip_dest = "/home/edonovan/projects/def-whkchun/memes/images/CA_2019Elections/twitter/Results"

#path_zip_dir = "/home/edonovan/projects/def-whkchun/memes/images/CA_2019Elections/twitter/twitter_fixed/"

# path to csv
path_csv = "/home/edonovan/projects/def-whkchun/memes/images/CA_2019Elections/twitter/twitter_filenames.csv"

zip_name = "twitter_fixed"
max_imgs_per_folder = 100000

###########################################################################

# file formats that we expects to see in zip
FileFormats = ['.jpg', '.png', '.gif']

counter = 0
files_moved_count = 0
folder_num = 1

# open csv file
df = pd.read_csv(path_csv)

name_col = df.filename
cols = pd.Series(name_col)

with zipfile.ZipFile(path_zip, 'r') as zip_ref:

   # create first folder
    dest_dir_path = path_zip_dest + "/folder_" + str(folder_num)

    if not os.path.exists(dest_dir_path):
        print("Creating new folder at " + dest_dir_path)
        files_moved_count = 0
        os.makedirs(dest_dir_path)

    #iterate through cols.values
    for file in cols.values:

        try:
            full_file = str(zip_name) + "/" + str(file)
            
            # ISSUE on CEDAR begins here. The error message is always: line 10: /home/edonovan : is a directory
            # It can't process the zip_ref.read(full_file).
            # I have tried to change the full_file to just be the file name and not the 'str(zip_name) + "/"' part before.
            # Nothing has worked so far. 
            # It's able to iterate through the entire CSV successfully. Just the ZipFile commands don't work.
            zip_ref.read(full_file)
            
            if files_moved_count < max_imgs_per_folder:
                try:
                    zip_ref.extract(full_file, dest_dir_path)
                except Exception as ex1:
                    print("File extraction process did not work.")
            else:
                folder_num += 1
                dest_dir_path = path_zip_dest + "/folder_" + str(folder_num)
                if not os.path.exists(dest_dir_path):
                    print("Creating new folder at " + dest_dir_path)
                    files_moved_count = 0
                    os.makedirs(dest_dir_path)
                try:
                    zip_ref.extract(full_file, dest_dir_path)
                except Exception as ex1:
                    print("File extraction process did not work.")
            files_moved_count += 1
        except Exception as ex2:
            continue
