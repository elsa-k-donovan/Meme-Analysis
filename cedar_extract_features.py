# Built by referencing 'image-search.ipynb' by Gene Kogan
import os
import keras
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import Model
import numpy as np
import matplotlib.pyplot as plt
import time
from sklearn.decomposition import PCA
import random
from scipy.spatial import distance
import pickle
import json
from PIL import Image
from sklearn.manifold import TSNE

## Hedayat: for cedar
import zipfile
import os
import glob

path_zip = "/Users/hedayattabesh/Documents/Data/Organic.zip"
path_zip_dest = "/Users/hedayattabesh/Documents/scripts/Meme-Analysis/data"
##

#from google.colab import drive
#drive.mount('/content/gdrive', force_remount=True)

#Research the different models and weights.
model = keras.applications.VGG16(weights='imagenet', include_top=True)

model.summary()

def load_image(path):
    img = image.load_img(path, target_size=model.input_shape[1:3])
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return img, x

# feature_extractor is the new name of feature extraction layer.
feat_extractor = Model(inputs=model.input, outputs=model.get_layer("fc2").output)

#Show details
feat_extractor.summary()

# Step 1: Change this to your file path.
images_path = "/Users/hedayattabesh/Documents/scripts/Meme-Analysis/data"

# Step 2: Choose image formats.
image_extensions = ['.jpg', '.png', '.jpeg', '.gif']   # case-insensitive (upper/lower doesn't matter)

## instead of retrieve image paths with this! lets grab it from the zip
## images = [os.path.join(dp, f) for dp, dn, filenames in os.walk(images_path) for f in filenames if os.path.splitext(f)[1].lower() in image_extensions]
# Lets open the zipfile so we can proccess
with zipfile.ZipFile(path_zip, 'r') as zip_ref:
    # lets get a list of all files in zip
    listOfFileNames_temp = zip_ref.namelist()
    images_zip = []
    # lets remove the non file paths
    for item in listOfFileNames_temp:
        for format_i in image_extensions:
            if format_i in item:
                images_zip.append(item)


    print("keeping %d images to analyze" % len(images_zip))


    tic = time.perf_counter()

    features = []


    for k in range(0, len(images_zip), 500):
        print("K=" + str(k))
        ## first lets extract and move the file we want
        if k+500 > len(images_zip):
            zip_ref.extractall(members=images_zip[k:len(images)], path=path_zip_dest)
        else:
            zip_ref.extractall(members=images_zip[k:k+500], path=path_zip_dest)
        ##
        images = [os.path.join(dp, f) for dp, dn, filenames in os.walk(images_path) for f in filenames if os.path.splitext(f)[1].lower() in image_extensions and not f[0] == '.' ]
        print(len(images))
        for i, image_path in enumerate(images):
            if i % 500 == 0:
                toc = time.perf_counter()
                elap = toc-tic
                print("analyzing image %d / %d. Time: %4.4f seconds." % (i, len(images),elap))
                tic = time.perf_counter()
            try:
                print(image_path)
                img, x = load_image(image_path)
            except Exception as ex1:
                print("Problem with file, may be corrupted.")
            # retrieve the feature vector of each image
            feat = feat_extractor.predict(x)[0]
            features.append(feat)
        
        # lets remove the current images 
        print("Removing all files!")
        os.system("rm -rfv ./data/*")

    print('finished extracting features for %d images' % len(images))

# features = np.array(features)

# #originally n_components=300
# pca = PCA(n_components=100)
# pca.fit(features)

# pca_features = pca.transform(features)

# # grab a random query image
# query_image_idx = int(len(images) * random.random())

# # let's display the image
# img = image.load_img(images[query_image_idx])
# plt.imshow(img)

# similar_idx = [distance.cosine(pca_features[query_image_idx], feat) for feat in pca_features ]

# idx_closest = sorted(range(len(similar_idx)), key=lambda k: similar_idx[k])[1:6]

# # load all the similarity results as thumbnails of height 100
# thumbs = []
# for idx in idx_closest:
#     img = image.load_img(images[idx])
#     img = img.resize((int(img.width * 100 / img.height), 100))
#     thumbs.append(img)

# # concatenate the images into a single image
# concat_image = np.concatenate([np.asarray(t) for t in thumbs], axis=1)

# # show the image
# plt.figure(figsize=(16,12))
# plt.imshow(concat_image)

# def get_closest_images(query_image_idx, num_results=5):
#     distances = [ distance.cosine(pca_features[query_image_idx], feat) for feat in pca_features ]
#     idx_closest = sorted(range(len(distances)), key=lambda k: distances[k])[1:num_results+1]
#     return idx_closest

# def get_concatenated_images(indexes, thumb_height):
#     thumbs = []
#     for idx in indexes:
#         img = image.load_img(images[idx])
#         img = img.resize((int(img.width * thumb_height / img.height), thumb_height))
#         thumbs.append(img)
#     concat_image = np.concatenate([np.asarray(t) for t in thumbs], axis=1)
#     return concat_image

# # do a query on a random image
# query_image_idx = int(len(images) * random.random())
# idx_closest = get_closest_images(query_image_idx)
# query_image = get_concatenated_images([query_image_idx], 300)
# results_image = get_concatenated_images(idx_closest, 200)

# # display the query image
# plt.figure(figsize = (5,5))
# plt.imshow(query_image)
# plt.title("query image (%d)" % query_image_idx)

# # display the resulting images
# plt.figure(figsize=(16,12))
# plt.imshow(results_image)
# plt.title("result images")

# #Save PCA-reduced features and array of images as a file using pickle
# pickle.dump([images, pca_features, pca], open(images_path + '/memes_beta_features.p', 'wb'))


# #new file

# images, pca_features, pca = pickle.load(open(images_path + '/memes_beta_features.p', 'rb'))

# for img, f in list(zip(images, pca_features))[0:5]:
#     print("image: %s, features: %0.2f,%0.2f,%0.2f,%0.2f... "%(img, f[0], f[1], f[2], f[3]))

# #num_images_to_plot = 1000

# # if len(images) > num_images_to_plot:
# #     sort_order = sorted(random.sample(range(len(images)), num_images_to_plot))
# #     images = [images[i] for i in sort_order]
# #     pca_features = [pca_features[i] for i in sort_order]

# X = np.array(pca_features)
# tsne = TSNE(n_components=2, learning_rate=150, perplexity=30, angle=0.2, verbose=2).fit_transform(X)

# tx, ty = tsne[:,0], tsne[:,1]
# tx = (tx-np.min(tx)) / (np.max(tx) - np.min(tx))
# ty = (ty-np.min(ty)) / (np.max(ty) - np.min(ty))

# width = 4000
# height = 3000
# max_dim = 100

# full_image = Image.new('RGBA', (width, height))
# for img, x, y in zip(images, tx, ty):
#     tile = Image.open(img)
#     rs = max(1, tile.width/max_dim, tile.height/max_dim)
#     tile = tile.resize((int(tile.width/rs), int(tile.height/rs)), Image.ANTIALIAS)
#     full_image.paste(tile, (int((width-max_dim)*x), int((height-max_dim)*y)), mask=tile.convert('RGBA'))

# plt.figure(figsize=(16,12))

# # Uncomment for saved image of tsne-map
# full_image.save("example-tSNE-all_reddit.png")

# # Save coordinates to JSON file for visualization.
# tsne_path = "memes-beta-features.json"

# data = [{"path":os.path.abspath(img), "point":[float(x), float(y)]} for img, x, y in zip(images, tx, ty)]
# with open(tsne_path, 'w') as outfile:
#     json.dump(data, outfile)

# print("saved t-SNE result to %s" % tsne_path)