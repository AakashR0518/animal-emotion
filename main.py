#import libs
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, BatchNormalization, Flatten, LeakyReLU, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing import image_dataset_from_directory
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from IPython.display import display, HTML, Javascript
import pathlib
import PIL
import tarfile
import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from keras.layers import TFSMLayer
from keras.models import Model
from keras.layers import Input
from tensorflow.keras.preprocessing import image
import os
from collections import defaultdict

class_names = ['angry', 'happy', 'relaxed', 'sad']

model = load_model('initial.h5',compile=False)

img_path = 'input-file-name'

class_counts = defaultdict(int)

# Load and preprocess the image
img = image.load_img(img_path, target_size=(384, 384))  # Adjust target_size to your model's input size
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
img_array /= 1./255.0  # Normalize if required by your model

predictions = model.predict(img_array)
predicted_class_index = np.argmax(predictions, axis=-1)

# Get the class name and update the count
predicted_class_name = class_names[predicted_class_index[0]]
class_counts[predicted_class_name] += 1

# Print the results
print(f'Class: {predicted_class_name}')