import numpy as np
import cv2
import os
import random
import math
import pickle
import matplotlib.pyplot as plt
from datetime import date, datetime
import skimage.io
import skimage.transform
import skimage.filters
import subprocess
import json
import pytz
import base64
import cv2
from PIL import Image
from io import BytesIO

# import tensorflow as tf
from tensorflow.keras  import backend as K
from tensorflow.keras.applications import VGG16
from tensorflow.keras import models, optimizers
from tensorflow.keras.models import Sequential, load_model, Model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, ZeroPadding2D, Convolution2D, AveragePooling2D, GlobalAveragePooling2D
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard, RemoteMonitor
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from tensorflow.keras.applications import DenseNet201, VGG19, VGG16, ResNet50
from tensorflow.keras.optimizers import RMSprop, Adam, SGD, Adamax

from app.queries import *

import time
basedir = os.path.abspath(os.path.dirname(__file__))

######## INISIALIASI VARIABEL GLOBAL #############################################################
LOKASI_MODEL = ''
LOKASI_CITRA = ''
LOKASI_DATASET = ''
HEIGHT = 100
WIDTH = 1200
TRAINING_SET = 0
VALIDATION_SET = 0
TRAIN_STEP = 0
VALID_STEP = 0
MODEL = Model()
PRETRAINED_MODEL = 0
OPTIMIZER = 0
CLASSES = []
JUMLAH_KELAS = 0

basedir = os.path.abspath(os.path.dirname(__file__))

#------------- FUNGSI DATASET ---------------------------------------------///

# visualisasi augmentasi


#------------- FUNGSI PELATIHAN ---------------------------------------------///


#------------- FUNGSI PENGUJIAN ---------------------------------------------///

# API Pengujian
