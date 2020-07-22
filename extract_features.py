# Built by referencing 'image-search.ipynb' by Gene Kogan

import os
import keras
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
from keras.models import Model
import numpy as np
import matplotlib.pyplot as plt
import time
from sklearn.decomposition import PCA
import random
from scipy.spatial import distance
import pickle

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

feat_extractor = Model(inputs=model.input, outputs=model.get_layer("fc2").output)
feat_extractor.summary()

# Step 1: Change this to your file path.
images_path = "/Volumes/External_HD/memes"

# Step 2: Choose image formats.
image_extensions = ['.jpg', '.png', '.jpeg', '.gif']   # case-insensitive (upper/lower doesn't matter)

images = [os.path.join(dp, f) for dp, dn, filenames in os.walk(images_path) for f in filenames if os.path.splitext(f)[1].lower() in image_extensions]

print("keeping %d images to analyze" % len(images))


tic = time.perf_counter()

features = []
for i, image_path in enumerate(images):
    if i % 500 == 0:
        toc = time.perf_counter()
        elap = toc-tic;
        print("analyzing image %d / %d. Time: %4.4f seconds." % (i, len(images),elap))
        tic = time.perf_counter()
    try:
        # removed img, x
        x = load_image(image_path)
    except Exception as ex1:
        print("Problem with file, may be corrupted.")
    feat = feat_extractor.predict(x)[0]
    features.append(feat)

print('finished extracting features for %d images' % len(images))

features = np.array(features)

#originally n_components=300
pca = PCA(n_components=100)
pca.fit(features)

pca_features = pca.transform(features)

# grab a random query image
query_image_idx = int(len(images) * random.random())

# let's display the image
# img = image.load_img(images[query_image_idx])
# plt.imshow(img)

similar_idx = [ distance.cosine(pca_features[query_image_idx], feat) for feat in pca_features ]

idx_closest = sorted(range(len(similar_idx)), key=lambda k: similar_idx[k])[1:6]

# load all the similarity results as thumbnails of height 100
thumbs = []
for idx in idx_closest:
    img = image.load_img(images[idx])
    img = img.resize((int(img.width * 100 / img.height), 100))
    thumbs.append(img)

# concatenate the images into a single image
concat_image = np.concatenate([np.asarray(t) for t in thumbs], axis=1)

# show the image
plt.figure(figsize=(16,12))
plt.imshow(concat_image)

def get_closest_images(query_image_idx, num_results=5):
    distances = [ distance.cosine(pca_features[query_image_idx], feat) for feat in pca_features ]
    idx_closest = sorted(range(len(distances)), key=lambda k: distances[k])[1:num_results+1]
    return idx_closest

def get_concatenated_images(indexes, thumb_height):
    thumbs = []
    for idx in indexes:
        img = image.load_img(images[idx])
        img = img.resize((int(img.width * thumb_height / img.height), thumb_height))
        thumbs.append(img)
    concat_image = np.concatenate([np.asarray(t) for t in thumbs], axis=1)
    return concat_image

# do a query on a random image
query_image_idx = int(len(images) * random.random())
idx_closest = get_closest_images(query_image_idx)
query_image = get_concatenated_images([query_image_idx], 300)
results_image = get_concatenated_images(idx_closest, 200)

# display the query image
plt.figure(figsize = (5,5))
plt.imshow(query_image)
plt.title("query image (%d)" % query_image_idx)

# display the resulting images
plt.figure(figsize = (16,12))
plt.imshow(results_image)
plt.title("result images")

#Save PCA-reduced features and array of images as a file using pickle
pickle.dump([images, pca_features, pca], open('/Volumes/External_HD/memes/memes_features.p', 'wb'))