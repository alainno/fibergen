import cv2
import numpy as np
from fiberrandom import FiberSample
from PIL import Image,ImageDraw,ImageOps
from random import randint

sample_height = 128
sample_width = 128

sample_image = np.zeros((sample_height,sample_width,3), np.uint8)

fiber_sample = FiberSample(sample_width, sample_height)
waves = fiber_sample.createRandomWaves(5)

for wave in waves:
  wave = np.array(wave).astype(int)
  wave = wave.reshape((-1,1,2))
  cv2.polylines(sample_image,[wave],False,(255,255,255), randint(1,3), cv2.LINE_AA)

cv2.imshow('polylines', sample_image)
cv2.waitKey(0)


#cv2.imshow('Sample', sample_image)
#cv2.waitKey(0)
