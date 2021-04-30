from random import randint
import cv2
import numpy as np
from fiberrandom import FiberSample
import os
import json
import random

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
        cv2.polylines(sample_image,[wave],False,(255,255,255),thickness,cv2.LINE_AA)
        sum_thickness += thickness
    return sum_thickness        
        
def drawSampleFibers(sample_image, waves, thickness_list, skeleton=False):
    '''
    dibuja las fibras ondeadas sobre una imagen
    '''    
    for i,wave in enumerate(waves):
        wave = np.array(wave).astype(int)
        wave = wave.reshape((-1,1,2))
        #thickness = randint(min_thickness,max_thickness)    
        color = (thickness_list[i],thickness_list[i],thickness_list[i]) if skeleton else (255,255,255)
        #cv2.polylines(sample_image,[wave],False,color,thickness_list[i],cv2.LINE_AA)
        thickness = 1 if skeleton else thickness_list[i]
        line = cv2.LINE_8 if skeleton else cv2.LINE_AA
        cv2.polylines(sample_image, [wave], False, color, thickness, cv2.LINE_8)

def createSamples(directory, size, samples, thickness, fibers, extension="png", printout=True):
    fiber_sample = FiberSample(size[0], size[1], printout)
    for i in range(0,samples):
        waves = fiber_sample.createRandomWaves(randint(fibers[0],fibers[1]))
        sample_image = np.zeros((size[0], size[1], 3), np.uint8)
        drawFibers(sample_image, waves, thickness[0], thickness[1])
        cv2.imwrite(directory + "/" + str(i + 1).zfill(4) + "." + extension, sample_image)

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

def createSamplesAndSkeletons(dir_samples, dir_skeletons, size, samples, thickness, fibers, extension="png", printout=True):
    
    fiber_sample = FiberSample(size[0], size[1], printout)
    
    for i in range(0,samples):
        waves = fiber_sample.createRandomWaves(randint(fibers[0],fibers[1]))
        
        sample_image = np.zeros((size[0], size[1], 3), np.uint8)
        drawFibers(sample_image, waves, thickness[0], thickness[1])
        
        skeleton_image = np.zeros((size[0], size[1], 3), np.uint8)
        drawFibers(skeleton_image, waves, 1, 1)
        
        cv2.imwrite(dir_samples + "/" + str(i + 1).zfill(4) + "." + extension, sample_image)
        cv2.imwrite(dir_skeletons + "/" + str(i + 1).zfill(4) + "." + extension, skeleton_image)
        
def createSamplesAndVariableSkeletons(
    dir_samples,
    dir_skeletons,
    size,
    total_samples,
    thickness_range,
    fibers_range,
    extension="png",
    printout=False):
    '''
    Create samples with respective skeletons with different values that represents fiber diameter
    '''
    
    fiber_sample = FiberSample(size[0], size[1], printout)
    
    for i in range(total_samples):
        
        print(f'i={i}')
        
        len_waves = randint(fibers_range[0],fibers_range[1])
        
        fiber_waves = fiber_sample.createRandomWaves(len_waves)
        
        thickness_list = []
        for _ in range(len_waves):
            thickness_list.append(randint(thickness_range[0],thickness_range[1]))
        #thickness_list = sorted(thickness_list)
        
        sample_image = np.zeros((size[0], size[1], 3), np.uint8)
        #drawFibers(sample_image, waves, thickness[0], thickness[1])
        drawSampleFibers(sample_image, fiber_waves, thickness_list)
        
        skeleton_image = np.zeros((size[0], size[1], 3), np.uint8)
        drawSampleFibers(skeleton_image, fiber_waves, thickness_list, True)
        
        cv2.imwrite(dir_samples + "/" + str(i + 1).zfill(4) + "." + extension, sample_image)
        cv2.imwrite(dir_skeletons + "/" + str(i + 1).zfill(4) + "." + extension, skeleton_image)
        

    

    