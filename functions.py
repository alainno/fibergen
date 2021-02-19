from random import randint
import cv2
import numpy as np
from fiberrandom import FiberSample
import os
import json

def emptyDir(folder):
    '''
    Eliminar archivos contenidos en 'folder'
    '''
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def drawFibers(sample_image, waves, min_thickness, max_thickness):
    sum_thickness = 0
    for wave in waves:
        wave = np.array(wave).astype(int)
        wave = wave.reshape((-1,1,2))
        thickness = randint(min_thickness,max_thickness)
        cv2.polylines(sample_image,[wave],False,(255,255,255), thickness, cv2.LINE_AA)
        sum_thickness += thickness
    return sum_thickness

def createSamples(directory, size, samples, thickness, fibers):
    fiber_sample = FiberSample(size[0], size[1])
    for i in range(0,samples):
        waves = fiber_sample.createRandomWaves(randint(fibers[0],fibers[1]))
        sample_image = np.zeros((size[0], size[1], 3), np.uint8)
        drawFibers(sample_image, waves, thickness[0], thickness[1])
        cv2.imwrite(directory + "/" + str(i + 1).zfill(4) + ".png", sample_image)

def createSamplesAndMetrics(directory, size, samples, thickness, fibers):
    fiber_sample = FiberSample(size[0], size[1])
    metrics = {}
    for i in range(0,samples):
        waves = fiber_sample.createRandomWaves(randint(fibers[0],fibers[1]))
        sample_image = np.zeros((size[0], size[1], 3), np.uint8)
        sum_thickness = drawFibers(sample_image, waves, thickness[0], thickness[1])
        sample_path = directory + "/" + str(i + 1).zfill(4) + ".png"
        cv2.imwrite(sample_path, sample_image)
        metrics[sample_path] = round(sum_thickness / len(waves), 2)
    with open(directory + "/metrics.json", 'w') as fp:
        json.dump(metrics, fp)
    

def initDirectory(path):
    if(os.path.isdir(path)):
        emptyDir(path)
    else:
        try:
            os.makedirs(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)

