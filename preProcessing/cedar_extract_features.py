# Built by referencing 'image-search.ipynb' by Gene Kogan
import os
import keras
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import Model
import numpy as np
import time
# from sklearn.decomposition import SparsePCA
from sklearn.decomposition import TruncatedSVD
import pickle
import json
from PIL import Image
from sklearn.manifold import TSNE
import zipfile
# import concurrent.futures
import pathlib
from scipy.sparse import csr_matrix ## for sparse matrix

def load_image(path):
    img = image.load_img(path, target_size=model.input_shape[1:3])
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return img, x

def proccess_images(zip_loc, dest_loc, model):
    with zipfile.ZipFile(zip_loc, 'r') as zip_ref:
        # lets get a list of all files in zip
        listOfFileNames_temp = zip_ref.namelist()
        images_zip = []
        # lets remove the non file paths
        for item in listOfFileNames_temp:
            for format_i in image_extensions:
                if format_i in item and not '/.' in item:
                    images_zip.append(item)

        print("keeping %d images to analyze" % len(images_zip))
        first_folder = pathlib.Path(images_zip[0]).parts[0]
        dest_loc_with_zip_name = dest_loc + "/" + first_folder

        tic = time.perf_counter()

        for k in range(0, len(images_zip), 200000):
            ## first lets extract and move the file we want
            if k+200000 > len(images_zip):
                zip_ref.extractall(members=images_zip[k:len(images_zip)], path=dest_loc)
            else:
                zip_ref.extractall(members=images_zip[k:k+200000], path=dest_loc)
            
            images = [os.path.join(dp, f) for dp, dn, filenames in os.walk(dest_loc_with_zip_name) for f in filenames if os.path.splitext(f)[1].lower() in image_extensions and not f[0] == '.' ]
            for i, image_path in enumerate(images):
                if i % 500 == 0:
                    toc = time.perf_counter()
                    elap = toc-tic
                    print("analyzing image %d / %d. Time: %4.4f seconds." % (i, len(images),elap))
                    tic = time.perf_counter()
                try:
                    img, x = load_image(image_path)
                except Exception as ex1:
                    print("Problem with file, may be corrupted.")
                # retrieve the feature vector of each image
                feat = model.predict(x)[0]
                features.append(feat)
                # produces generator for future use <- 
                # yield feat # <----- TODO: google 
            
            # lets remove the current images 
            print("Removing all files!")
            os.system("rm -rf " + dest_loc_with_zip_name)

    # print('finished extracting features for %d images' % len(images_zip))
    return features, images_zip

time.sleep(10)

# Step 1: Change this to your file path.
# # personal
# images_path = "/Users/hedayattabesh/Documents/scripts/Meme-Analysis/data"
# dec_loc = images_path
# cedar
images_path = "/home/htabesh/projects/def-whkchun/memes/images/CA_2019Elections"
dec_loc = "/home/htabesh/scratch/data"

file_name_suffix = "full"

#Research the different models and weights.
model = keras.applications.VGG16(weights='imagenet', include_top=True)
model.summary()

# feature_extractor is the new name of feature extraction layer.
feat_extractor = Model(inputs=model.input, outputs=model.get_layer("fc2").output)

#Show details
feat_extractor.summary()

# Step 2: Choose image formats.
image_extensions = ['.jpg', '.png', '.jpeg', '.gif']   # case-insensitive (upper/lower doesn't matter)

zips = [os.path.join(dp, f) for dp, dn, filenames in os.walk(images_path) for f in filenames if os.path.splitext(f)[1].lower() == ".zip"]

print("keeping %d zips to analyze" % len(zips))
print(zips)

features = []
images = []
threads = []
return_value = []
# with concurrent.futures.ThreadPoolExecutor() as executor:
    # # lets create a thread per zip
for zip_i in zips:
    return_value.append(proccess_images(zip_i, dec_loc, feat_extractor))
    # threads.append(executor.submit(proccess_images, zip_i, dec_loc, feat_extractor))
# # lets get the return value of each thread
# for thread_i in threads:
#     return_value.append(thread_i.result())

for ret_i in return_value:
    features = features + ret_i[0]
    images = images + ret_i[1]

print("length of features is " + str(len(features)))
print("length of images is " + str(len(images)))

# lets checkpoint it here
with open(dec_loc + '/memes_checkpoint_features_' + file_name_suffix + '.txt', 'w') as f:
    for item in features:
        f.write("%s\n" % item)
with open(dec_loc + '/memes_checkpoint_images_' + file_name_suffix + '.txt', 'w') as f:
    for item in images:
        f.write("%s\n" % item)

# features = csr_matrix(features) # <- scipy
# # <- TODO: make sparse matrix
# # features = np.array(features)

# # csr sparse matrix
# pca = TruncatedSVD(n_components=.95,random_state=0)
# pca.fit(features)

# pca_features = pca.transform(features)

# #Save PCA-reduced features and array of images as a file using pickle
# pickle.dump([images, pca_features, pca], open(dec_loc + '/memes_features_' + file_name_suffix + '.p', 'wb'))

# #new file
# images, pca_features, pca = pickle.load(open(dec_loc + '/memes_features_' + file_name_suffix + '.p', 'rb'))

# for img, f in list(zip(images, pca_features))[0:5]:
#     print("image: %s, features: %0.2f,%0.2f,%0.2f,%0.2f... "%(img, f[0], f[1], f[2], f[3]))

# X = np.array(pca_features)
# tsne = TSNE(n_components=2, learning_rate=150, perplexity=30, angle=0.2, verbose=2).fit_transform(X)

# tx, ty = tsne[:,0], tsne[:,1]
# tx_norm = (tx-np.min(tx)) / (np.max(tx) - np.min(tx))
# ty_norm = (ty-np.min(ty)) / (np.max(ty) - np.min(ty))

# # Save coordinates to JSON file for visualization.
# tsne_path_norm =  dec_loc + "/norm-memes-beta-features-" + file_name_suffix + ".json"
# tsne_path = dec_loc + "/memes-beta-features-" + file_name_suffix + ".json"

# data = [{"path":os.path.abspath(img), "point":[float(x), float(y)]} for img, x, y in zip(images, tx_norm, ty_norm)]
# with open(tsne_path_norm, 'w') as outfile:
#     json.dump(data, outfile)

# data = [{"path":os.path.abspath(img), "point":[float(x), float(y)]} for img, x, y in zip(images, tx, ty)]
# with open(tsne_path, 'w') as outfile:
#     json.dump(data, outfile)

# print("saved t-SNE result to %s" % tsne_path)