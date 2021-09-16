'''
Show the phase abberation calculated across a range of z values

'''
import numpy as np
import cv2

imageFileName='blep_raw.jpg'
DELAY=200            # pause display using waitKey
z = 820             # height of object above image sensor (in microns)
dxy   = 1.4e-6      # imager pixel size in meters.
wvlen = 650.0e-9    # red laser wavelength (meters)
zScale=1e-6         # convert z units to microns

M=500; N = 500;
_x1 = np.arange(0,N/2)
_x2 = np.arange(N/2,0,-1)
_y1 = np.arange(0,M/2)
_y2 = np.arange(M/2,0,-1)
_x  = np.concatenate([_x1, _x2])
_y  = np.concatenate([_y1, _y2])
x, y  = np.meshgrid(_x, _y)
kx,ky = x / (dxy * N), y / (dxy * M)
kxy2  = (kx * kx) + (ky * ky)

# compute phase aberration
for z in range(100,2000,20):
    phAbbr   = np.exp(-1j * np.pi * wvlen * z * zScale * kxy2)
    realIM=(np.real(phAbbr)) 
    phaseIM=np.zeros((M,N),dtype='uint8')    # make blank image
    phaseIM= cv2.normalize(realIM,  phaseIM, 0, 255, cv2.NORM_MINMAX)
    phaseIM=phaseIM.astype('uint8') # convert int32 to uint8 for dispaly
    cv2.imshow('phaseAbb',phaseIM)
    cv2.waitKey(DELAY)
cv2.waitKey(DELAY)
cv2.destroyAllWindows()



