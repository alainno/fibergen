import cv2
import numpy as np
from fiberrandom import FiberSample
from PIL import Image,ImageDraw,ImageOps
from random import randint
from functions import *

sample_height = 128
sample_width = 128

#cv2.imshow('polylines', sample_image)
#cv2.waitKey(0)
DATA_DIR = "data"
TRAIN_DIR = "train"
VAL_DIR = "validation"
THIN_DIR = "thin"
THICK_DIR = "thick"

thin_directory = os.path.join(os.getcwd(), DATA_DIR, TRAIN_DIR, THIN_DIR)
train_samples = 10
thin_thickness = (1,3)
sample_fibers = (2,20)
sample_size = (sample_width, sample_height)

#
initDirectory(thin_directory)
createSamples(thin_directory, sample_size, train_samples, thin_thickness, sample_fibers)

#
thick_directory = os.path.join(os.getcwd(), DATA_DIR, TRAIN_DIR, THICK_DIR)
thick_thickness = (4,7)
initDirectory(thick_directory)
createSamples(thick_directory, sample_size, train_samples, thick_thickness, sample_fibers)

#
thin_directory_val = os.path.join(os.getcwd(), DATA_DIR, VAL_DIR, THIN_DIR)
val_samples = 2
initDirectory(thin_directory_val)
createSamples(thin_directory_val, sample_size, val_samples, thin_thickness, sample_fibers)

#
thick_directory_val = os.path.join(os.getcwd(), DATA_DIR, VAL_DIR, THICK_DIR)
initDirectory(thick_directory_val)
createSamples(thick_directory_val, sample_size, val_samples, thick_thickness, sample_fibers)
