from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
from keras.preprocessing import image
import os
import shutil
from IPython.display import display
from PIL import Image

#paths to dataset
train_data_dir = "C:/Users/elsa/Downloads/dataset/fb_training_set"
test_data_dir = "C:/Users/elsa/Downloads/dataset/reddit_test_set"


# Initialize the CNN
classifier = Sequential()

#Step 1 - Convolution
classifier.add(Conv2D(32, 3, 3, input_shape=(64, 64, 3), activation='relu'))

#Step 2 - Pooling
classifier.add(MaxPooling2D(pool_size=(2, 2)))

#Step 3 - Flattening
classifier.add(Flatten())

#Step 4 - Full Connection
classifier.add(Dense(output_dim=128, activation='relu'))
classifier.add(Dense(output_dim=1, activation='sigmoid'))

#Compiling the CNN
classifier.compile(optimizer='adam', loss= 'binary_crossentropy', metrics =['accuracy'])



# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1. / 255)

training_set = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(64, 64),
    batch_size=32,
    class_mode='binary')

test_set = test_datagen.flow_from_directory(
    test_data_dir,
    target_size=(64, 64),
    batch_size=32,
    class_mode='binary')

classifier.fit_generator(
    training_set,
    #originally 8000
    steps_per_epoch=800,
    #originally like 12
    epochs=2,
    validation_data=test_set,
    validation_steps=800)


#load directory of Reddit images here.
#create new folder if meme and insert file in

folder_path = "C:/Users/elsa/Downloads/Reddit/Reddit"

new_meme_dir = "memes"
new_non_meme_dir = "non-memes"

try:
    os.mkdir(new_meme_dir)
    os.mkdir(new_non_meme_dir)

except OSError:
    print("Creation of the directory %s failed")
else:
    print("Successfully created folder")



for img in os.listdir(folder_path):

    print(img)
    img = folder_path + "/" + img

    test_image = image.load_img(img, target_size=(64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = classifier.predict(test_image)
    training_set.class_indices

    if result[0][0] >= 0.5:
        #mkdir non-meme
        prediction = 'not a meme'
        shutil.copy(img, new_non_meme_dir)
    else:
        #mkdir meme
        prediction = 'meme'
        shutil.copy(img, new_meme_dir)

    print("This image is a " + prediction + ".")


