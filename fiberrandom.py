from PIL import Image,ImageDraw,ImageOps
from random import randint
import math
import numpy as np
from tqdm import tqdm
import os, shutil
import cv2
import colorsys

class FiberSample():
    '''
    Clase para generar imágenes artificiales de fibra de alpaca
    '''
    def __init__(self, width=256, height=256, printout=True):
        self.width = width
        self.height = height
        #print("Width: ", str(self.witdh))
        self.printout = printout

    def perpendicular_y(self,m,x1,y1,x):
        return (y1 - (x - x1)/m)

    def perpendicular_x(self,m,x1,y1,y):
        return (x1 - (y - y1)*m)

    def perpendicular_line(self, dx, dy):
        points = []
        m = dy / dx
        cx, cy = self.width / 2, self.height / 2
        x1, y1 = cx + dx, cy + dy

        if self.printout:
            print('x1:', x1, 'y1:', y1)

        x = 0
        y = self.perpendicular_y(m, x1, y1, x)

        if(y < 0 or y > self.height):
            x = self.perpendicular_x(m, x1, y1, y)
            if(y<0):
                y=0
            elif(y>self.height):
                y=self.height

        points.append((round(x),round(y)))

        x = self.width
        y = self.perpendicular_y(m, x1, y1, x)

        if (y < 0 or y > self.height):
            x = self.perpendicular_x(m, x1, y1, y)
            if (y < 0):
                y = 0
            elif (y > self.height):
                y = self.height

        points.append((round(x), round(y)))
        return points


    def fiberLine(self, dx, dy):
        #centro = self.width / 2, self.height / 2
        cx, cy = self.width / 2, self.height / 2

        #x, y = centro[0] + dx, centro[1] + dy
        x, y = cx + dx, cy + dy
        m = dy / dx

        if (dx < 0):
            ox = 0
        else:
            ox = self.width

        if (dy < 0):
            oy = 0
        else:
            oy = self.height

        y_ = y - (ox - x) / m
        x_ = x - (oy - y) * m

        return [(ox, y_), (x_, oy)]

    def randValue(self,limit):
        return randint(1, limit)

    def createRandomLines(self, total):
        lines = []
        xlimit = self.width / 2
        ylimit = self.height / 2

        for i in range(total):
            mod = i%4
            if(mod==0):
                lines.append(self.fiberLine(-self.randValue(xlimit), -self.randValue(ylimit)))
            elif(mod==1):
                lines.append(self.fiberLine(-self.randValue(xlimit), self.randValue(ylimit)))
            elif(mod==2):
                lines.append(self.fiberLine(self.randValue(xlimit), -self.randValue(ylimit)))
            elif(mod==3):
                lines.append(self.fiberLine(self.randValue(xlimit), self.randValue(ylimit)))

        return lines

    def drawFibers(self, img, lines, min_width, max_width):
        draw = ImageDraw.Draw(img)
        for line in lines:
            draw.line(line, fill=(255, 255, 255), width=randint(min_width,max_width))

    def createFiberSample(self, fiber_number, min_width, max_width):
        img = Image.new('RGB', (self.width, self.height), "black")
        lines = self.createRandomLines(fiber_number)
        self.drawFibers(img, lines, min_width, max_width)
        return img

    def createRandomLine(self):
        xlimit = self.width / 2
        ylimit = self.height / 2
        cuadrante_a = 1 - randint(0, 1)*2
        cuadrante_b = 1 - randint(0, 1)*2
        #print('cuadrante a:',cuadrante_a)
        #print('cuadrante b:',cuadrante_b)

        # las distancias dx,dy como maximo seran 1 menor al limite sino se creara una perpendicular de tamaño 0
        dx = self.randValue(xlimit-1)*cuadrante_a
        dy = self.randValue(ylimit-1)*cuadrante_b

        if self.printout:
            print('dx:', dx, 'dy:', dy)

        return [(xlimit, ylimit), (dx+xlimit, dy+ylimit)]


    def getPerpendicular(self, line):
        points = []

        cx, cy = line[0]
        x1, y1 = line[1]

        m = (y1-cy) / (x1-cx)

        if self.printout:
            print('m:', m)
            print('x1:', x1)
            print('y1:', y1)

        x = 0
        y = self.perpendicular_y(m, x1, y1, x) # y1 - (x - x1) / m

        if (y < 0):
            y = 0
            x = self.perpendicular_x(m, x1, y1, y) # x1 - (y - y1) * m
        elif (y > self.height):
            y = self.height
            x = self.perpendicular_x(m, x1, y1, y)

        points.append((round(x), round(y)))

        x = self.width
        y = self.perpendicular_y(m, x1, y1, x) 

        if (y < 0):
            y = 0
            x = self.perpendicular_x(m, x1, y1, y)
        elif (y > self.height):
            y = self.height
            x = self.perpendicular_x(m, x1, y1, y)

        points.append((round(x), round(y)))
        return points

    def createFiberWavedSample(self, fiber_number, min_width, max_width):
        img = Image.new('RGB', (self.width, self.height), "black")
        waves = self.createRandomWaves(fiber_number)
        self.drawWavedFibers(img, waves, min_width, max_width)
        return img

    def drawWavedFibers(self, img, waves, min_width, max_width):
        draw = ImageDraw.Draw(img)
        for wave_points in waves:
            draw.line(wave_points, fill=(255, 255, 255), width=randint(min_width, max_width))

    def createRandomWaves(self, total):
        waves = []

        #waves.append([1, 1, 20, 20, 30, 30, 40, 40])
        #waves.append([50, 1, 70, 20, 80, 30, 90, 40])

        for i in range(total):
            ancho = randint(3, 6)/100
            alto = (randint(5,60)/100)/ancho
            waves.append(self.createFiberWave(ancho, alto))
        return waves

    def createFiberWave(self, ancho=0.05, alto=5):

        #fiberSample = FiberSample(256, 256)
        # trazar una línea aleatoria con u radomness
        points = self.createRandomLine()
        #print('Recta aleatoria:', points)

        perp_points = self.getPerpendicular(points)
        if self.printout:
            print('Recta perpendicular:', perp_points)

        # trazar onda senoidal
        # obtener la longitud de la recta aleatoria (time)
        distance = self.getDistance(perp_points)
        if self.printout:
            print('distance:', round(distance))
        time = np.arange(0, distance, 1)
        # print('time:', time)

        # generar amplitud
        #amplitude = np.sin(0.05 * time)
        amplitude = np.sin(ancho * time)
        # print('amplitud:', amplitude)

        # obtener angulo de la recta aleatoria
        x1, y1 = perp_points[0]
        x2, y2 = perp_points[1]
        m = (y2 - y1) / (x2 - x1)
        angle = math.atan(m)
        if self.printout:
            print('angle:', math.degrees(angle))

        # rotar

        sine_points = []
        rotated_points = []
        #pond = 5
        pond = alto
        #mitad = fiberSample.height / 2

        for i, a in enumerate(amplitude):
            sine_points.append(time[i] + x1)
            sine_points.append(y1 - round(a * pond))

            point = self.rotate((0, 0), (time[i], round(a * pond)), -angle)

            rotated_points.append(point[0] + x1)
            rotated_points.append(y1 - point[1])

        return rotated_points

    # obtiene la distancia euclideana entre dos puntos
    def getDistance(self, line):
        x1, y1 = line[0]
        x2, y2 = line[1]
        return math.sqrt((x2-x1)**2 + (y2-y1)**2)

    def rotate(self, origin, point, angle):
        """
        Rotate a point counterclockwise by a given angle around a given origin.
        The angle should be given in radians.
        """
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy

    def getWavePoints(self):
        pass
    
    def setFibers(self,fibers):
        self.fibers = fibers
    
    def setDiameters(self, diameters):
        self.diameters = diameters
    
    def createSegmentationSample(self):
        self.segmentation_img = Image.new('RGB', (self.width,self.height), 'white')
        draw = ImageDraw.Draw(self.segmentation_img)
        self.segmentation_mask = np.zeros((self.height, self.width, 3), np.uint8)
        
        waves_number = randint(self.fibers[0], self.fibers[1])
        waves = self.createRandomWaves(waves_number)
        
        for wave in waves:
            diameter = randint(self.diameters[0], self.diameters[1])
            gray = randint(0,100)
            
            draw.line(wave, fill=(gray, gray, gray), width=diameter, joint='curve')
    
            wave = np.array(wave).astype(int)
            wave = wave.reshape((-1,1,2))
            cv2.polylines(self.segmentation_mask,[wave],False,(255,255,255),diameter,cv2.LINE_AA)
                
    
    def saveSegmentationSample(self, imgs_dir, masks_dir, index, extension='png'):
        '''
        Guarda la imágen y su máscara de segmentación
        '''
        #self.segmentation_img = Image.new('RGB', (5, 5), "white")
        filename = str(index+1).zfill(4) + '.' + extension
        self.segmentation_img.save(os.path.join(imgs_dir, filename))
        #self.segmentation_mask = np.zeros((5,5,3), np.uint8)
        cv2.imwrite(os.path.join(masks_dir, filename), self.segmentation_mask)
        
    def createDistanceMapSample(self):
        size = (self.height, self.width, 3)

        self.dm_img = np.zeros(size, np.uint8)
        self.dm_mask = np.zeros(size, np.uint8)

        fibers = randint(self.fibers[0],self.fibers[1])
        waves = self.createRandomWaves(fibers)

        colors = self.randcolors(fibers)

        for i,wave in enumerate(waves):
            diameter = randint(self.diameters[0], self.diameters[1])
            
            wave = np.array(wave).astype(int)
            wave = wave.reshape((-1,1,2))
            
            #cv2.polylines(self.dm_img, [wave], False, colors[i], diameter, cv2.LINE_8)
            
            image = np.zeros((256,256,1), np.uint8)
            cv2.polylines(image,[wave],False,(255,255,255),diameter,cv2.LINE_AA)
            
            lbl = image.copy()
            lbl = lbl.reshape(256,256)
            col = self.TruncatedNormal(loc=127, scale=100, size=3, min_v=1, max_v=255)
            nrow = lbl[lbl==255].shape[0]
            RANDOM = np.zeros(shape=(nrow, 3))
            for j in range(3):
                RANDOM[:, j] = self.TruncatedNormal(loc=col[j], scale=10, size=nrow, min_v=1, max_v=255)
            self.dm_img[lbl==255] = RANDOM
            
            
            image = cv2.distanceTransform(image,cv2.DIST_L2,3)
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            foreground = image[:,:]>0
            self.dm_mask[foreground] = image[foreground]
        
        self.dm_img = self.Noise(self.dm_img, 5)
        cv2.normalize(self.dm_mask, self.dm_mask, 0, 255, cv2.NORM_MINMAX)
            
    def saveDistanceMapSample(self, imgs_dir, masks_dir, index, extension='png'):
        '''
        Guarda la imágen y su máscara (mapa de distancia)
        '''
        filename = str(index+1).zfill(4) + '.' + extension
        cv2.imwrite(os.path.join(imgs_dir, filename), self.dm_img)
        cv2.imwrite(os.path.join(masks_dir, filename), self.dm_mask)
        
    def randcolors(self, n):
        '''
        Se obtiene una lista de 'n' colores usando HSV
        '''
        colors = []
        for h in range(0, 360, int(360/n)):
            color = tuple(round(i) for i in colorsys.hsv_to_rgb(h/360,1,255))
            colors.append(color)
        return colors
    
    def TruncatedNormal(self, loc, scale, size, min_v, max_v):
        vec = np.random.normal(loc=loc, scale=scale, size=size)
        def f(val):
            if min_v > val:
                return True
            elif val > max_v:
                return True
            else:
                return False
        res = np.array(map(f, vec))
        if True in res:
            n_size = res.sum()
            vec[res] = TruncatedNormal(loc, scale, n_size, min_v, max_v)
        return vec
    
    def Noise(self, img, std):
        fl = img.flatten()
        vec = np.random.normal(loc=0, scale=std, size=len(fl))
        def g(val):
            if 0 > val:
                return -val
            else:
                return val
        noise = list(map(g, vec))
        noise = np.array(noise)
        res = fl + noise
        res = res.reshape(img.shape)
        res[res > 255.] = 255.
        return res.astype('uint8')


if __name__ == "__main__":

    from functions import emptyDir
    
    fiberSample = FiberSample(256,256)
    #createFiberImage(size, width, testDir)

    print('Generate fiber sample with random widths')

    #img = fiberSample.createFiberSample(10, 1, 5)
    img = fiberSample.createFiberWavedSample(10, 2, 12)
    img = ImageOps.invert(img)
    #img.save("img/sample-artificial.png", "PNG")
    img.show()

    

    
    '''
    testDir = "data/test"
    emptyDir(testDir)

    for i in range(20):
        img = fiberSample.createFiberWavedSample(16, i+1, i+1)
        img.save(testDir + "/" + str(i + 1).zfill(4) + ".png", "PNG")
    
        
    trainDir = "data_wave/train"
    valDir = "data_wave/validation"
    thinDir = "/thin"
    thickDir = "/thick"
    
    fibers = 16
    thin_width = 4
    thick_width = 12
    
    emptyDir(trainDir + thinDir)
    emptyDir(trainDir + thickDir)
    
    for i in tqdm(range(1000)):
        fibers = randint(1,16)
        img = fiberSample.createFiberWavedSample(fibers, 1, 8)
        img.save(trainDir + thinDir + "/" + str(i + 1).zfill(4) + ".png", "PNG")
        
        fibers = randint(1,16)
        img = fiberSample.createFiberWavedSample(fibers, 9, 16)
        img.save(trainDir + thickDir + "/" + str(i + 1).zfill(4) + ".png", "PNG")
        
    emptyDir(valDir + thinDir)
    emptyDir(valDir + thickDir)
    
    for i in tqdm(range(200)):
        fibers = randint(1,16)
        img = fiberSample.createFiberWavedSample(fibers, 1, 8)
        img.save(valDir + thinDir + "/" + str(i + 1).zfill(4) + ".png", "PNG")
        
        fibers = randint(1,16)
        img = fiberSample.createFiberWavedSample(fibers, 9, 16)
        img.save(valDir + thickDir + "/" + str(i + 1).zfill(4) + ".png", "PNG")
        
    '''

