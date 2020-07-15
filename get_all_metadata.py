import os

# Step 1: Add the filepath to your directory of images to see existing metadata.
# This way you can take a look at all the existing metadata and see which tags you want to extract.
img_folder = "/Volumes/External_HD/memes/"

command_h = "exiftool -csv -r " + img_folder + " > all_metadata.csv"

os.system(command_h)