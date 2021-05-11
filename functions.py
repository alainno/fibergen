from random import randint
import cv2
import numpy as np
from fiberrandom import FiberSample
import os
import json
import random
import colorsys

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
    '''
    se dibujan las fibras y se suma todos los grosores (diametros)
    retorna la suma
    '''
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
    dibuja las fibras ondeadas sobre una imagen completas o tan solo su esqueleto con el valor de su grosor
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
    Create samples with respective skeletons with different pixel values that represents fiber diameter
    '''
    
    fiber_sample = FiberSample(size[0], size[1], printout)
    
    for i in range(total_samples):
        
        #print(f'i={i}')
        
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
        
def randcolors(n):
    '''
    Se obtiene una lista de 'n' colores usando HSV
    '''
    colors = []
    for h in range(0, 360, int(360/n)):
        color = tuple(round(i) for i in colorsys.hsv_to_rgb(h/360,1,255))
        colors.append(color)
    return colors       
        
def drawSampleAndMask(sample_image, mask_image, waves, fiber_thickness):
    colors = randcolors(len(waves))
    for i,wave in enumerate(waves):
        wave = np.array(wave).astype(int)
        wave = wave.reshape((-1,1,2))
        color_sample = (255,255,255)
        color_mask = colors[i]
        thickness = randint(fiber_thickness[0],fiber_thickness[1])
        cv2.polylines(sample_image, [wave], False, color_sample, thickness, cv2.LINE_8)
        cv2.polylines(mask_image, [wave], False, color_mask, thickness, cv2.LINE_8)

def createSamplesAndMasks(samples_dir,masks_dir,samples,sample_size,sample_fibers,fiber_thickness,extension='png',printout=False):
    
    sample = FiberSample(sample_size[0], sample_size[1], printout)
    
    for i in range(samples):

        sample_image = np.zeros((sample_size[0], sample_size[1], 3), np.uint8)
        mask_image = np.zeros((sample_size[0], sample_size[1], 3), np.uint8)
        
        waves = sample.createRandomWaves(randint(sample_fibers[0],sample_fibers[1]))
        drawSampleAndMask(sample_image, mask_image, waves, fiber_thickness)
    
        cv2.imwrite(samples_dir + "/" + str(i + 1).zfill(4) + "." + extension, sample_image)
        cv2.imwrite(masks_dir + "/" + str(i + 1).zfill(4) + "." + extension, mask_image)