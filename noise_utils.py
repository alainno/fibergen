from skimage.measure import label
import numpy as np
import sys

def TruncatedNormal(loc, scale, size, min_v, max_v):
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

#col = TruncatedNormal(loc=127, scale=100, size=3, min_v=1, max_v=255)
#print(col)
def AddNoise(GT, mu, std, std_2, min_v, max_v):
    GT_lbl = label(GT)
    x, y = GT.shape
    GT_noise = np.zeros(shape=(x, y, 3))
    
    
    for i in range(1, GT_lbl.max() + 1):

        col = TruncatedNormal(loc=mu, scale=std, size=3, min_v=min_v, max_v=max_v)
        
        print('type col:', type(col))
        
        #GT_noise[GT_lbl == i] = col.astype(int)
        nrow = GT_lbl[GT_lbl == i].shape[0]
        
        print('nrow:', nrow)
        
        RANDOM = np.zeros(shape=(nrow, 3))
        
        print(f'random shape: {RANDOM.shape}')
        
        for j in range(3):
            RANDOM[:, j] = TruncatedNormal(loc=col[j], scale=std_2, size=nrow, min_v=min_v, max_v=max_v)
        
        GT_noise[GT_lbl == i] = RANDOM
        #sys.exit(0)

    return GT_noise.astype('uint8')

def AddNoiseFiber(fiber):
    lbl = fiber.copy()
    # lbl = lbl.reshape(256,256)
    col = TruncatedNormal(loc=127, scale=100, size=3, min_v=1, max_v=255)
    nrow = lbl[lbl==255].shape[0]
    RANDOM = np.zeros(shape=(nrow, 3))
    for j in range(3):
        RANDOM[:, j] = TruncatedNormal(loc=col[j], scale=10, size=nrow, min_v=1, max_v=255)
    return RANDOM


def Noise(img, std):
    fl = img.flatten()
    vec = np.random.normal(loc=0, scale=std, size=len(fl))
    def g(val):
        if 0 > val:
            return -val
        else:
            return val
    #noise = np.array(map(g, vec))
    noise = list(map(g, vec))
    #noise = np.fromiter(noise, dtype=np.float64)
    noise = np.array(noise)
    #print(noise.shape)
    #print("*****", fl.shape, "***", vec.shape)
    res = fl + noise
    #res = fl + vec
    res = res.reshape(img.shape)
    res[res > 255.] = 255.
    return res.astype('uint8')