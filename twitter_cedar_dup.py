import zipfile
import os
import pandas as pd
import shutil


###########################################################################
# Change all of the paths and variables in this section
# for batch processing on Cedar.

root = "/Volumes/Elsa_HD2/Memes/"

# path to zip file
#path_zip = "/home/edonovan/projects/def-whkchun/memes/images/CA_2019Elections/twitter/twitter_fixed.zip"
path_zip = "/Volumes/Elsa_HD2/Memes/fb_test.zip"

#path_zip_dest = "/home/edonovan/projects/def-whkchun/memes/images/CA_2019Elections/twitter/Results"
path_zip_dest = "/Volumes/Elsa_HD2/Memes/Twitter/Results/"
#path_zip_dir = "/home/edonovan/projects/def-whkchun/memes/images/CA_2019Elections/twitter/twitter_fixed/"

# path to csv
#path_csv = "/home/edonovan/projects/def-whkchun/memes/images/CA_2019Elections/twitter/twitter_filenames.csv"

path_csv = "/Volumes/Elsa_HD2/Memes/Twitter/twitter_filenames.csv"

zip_name = "fb_test"
max_imgs_per_folder = 1

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


def make_archive(source, destination):
    base = os.path.basename(destination)
    name = base.split('.')[0]
    format = base.split('.')[1]
    archive_from = os.path.dirname(source)
    archive_to = os.path.basename(source.strip(os.sep))
    shutil.make_archive(name, format, archive_from, archive_to)
    shutil.move('%s.%s' % (name, format), destination)


with zipfile.ZipFile(path_zip, 'r') as zip_ref:

   # create first folder
    dest_dir_path = path_zip_dest + "folder_" + str(folder_num)

    if not os.path.exists(dest_dir_path):
        print("Creating new folder at " + dest_dir_path)
        files_moved_count = 0
        os.makedirs(dest_dir_path)

    #iterate through cols.values
    for file in cols.values:
        try:
            full_file = str(zip_name) + "/" + str(file)
            zip_ref.read(full_file)

            if files_moved_count < max_imgs_per_folder:
                try:
                    print("before extract")
                    zip_ref.extract(full_file, dest_dir_path)
                except Exception as ex1:
                    print("File extraction process did not work.")
            else:
                folder_num += 1
                dest_dir_path = path_zip_dest + "folder_" + str(folder_num)
                if not os.path.exists(dest_dir_path):
                    print("Creating new folder at " + dest_dir_path)
                    files_moved_count = 0
                    os.makedirs(dest_dir_path)
                try:
                    zip_ref.extract(full_file, dest_dir_path)
                except Exception as ex1:
                    print("File extraction process did not work.")
            files_moved_count += 1
            print(files_moved_count)

            if files_moved_count >= max_imgs_per_folder:
                new_path_dest = path_zip_dest + "zip_folder" + str(folder_num) + ".zip"
                #it is zipping the Results folder instad of specific folder num
                print(dest_dir_path)
                try:
                    make_archive(dest_dir_path, new_path_dest)
                except Exception as ex0:
                    print("zip file didn't work")
                shutil.rmtree(dest_dir_path)
        except Exception as ex2:
            continue
