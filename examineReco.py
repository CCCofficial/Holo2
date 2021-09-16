'''
Break down the reconstruction code into steps and visualize to get a better understanding of how it works

Tom Zimmerman CCC, IBM Research September 16, 2020
This work is funded by the National Science Foundation (NSF) grant No. DBI-1548297, Center for Cellular Construction.
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation.
'''
import numpy as np
import cv2

imageFileName='blep_raw.jpg'
DELAY=0             # pause display using waitKey
z = 820             # height of object above image sensor (in microns)
dxy   = 1.4e-6      # imager pixel size in meters.
wvlen = 650.0e-9    # red laser wavelength (meters)
zScale=1e-6         # convert z units to microns

cropIM = cv2.imread(imageFileName, 0) #Read the image as grayscale

#make even coordinates
(yRez,xRez)=cropIM.shape
if (xRez%2)==1:
    xRez-=1
if (yRez%2)==1:
    yRez-=1
cropIM=cropIM[0:yRez,0:xRez]

# get square root of image
print('='*80)
print('Take square root of image and show image dimension')
sqrtIM = np.sqrt(cropIM)	 #calculate wavefront at z
M, N = sqrtIM.shape # get image size, rows M, columns N, they must be even numbers!
print('sqrtIM shape',sqrtIM.shape)
print('M (y axis) =',M,'  N (x axis) =',N)
sqrtImage=sqrtIM.astype('uint8') # convert to unsigned int 8 bit for display
normIM=np.zeros((M,N),dtype='uint8')    # make blank image
normIM= cv2.normalize(sqrtImage,  normIM, 0, 255, cv2.NORM_MINMAX)
cv2.imshow('sqrt',normIM)
cv2.imshow('raw',cropIM)
cv2.waitKey(DELAY)      # stop here until image closed

# prepare grid in frequency space with origin at 0,0
print('='*80)
print('Prepare grid in frequency space with origin at 0,0')
_x1 = np.arange(0,N/2)
_x2 = np.arange(N/2,0,-1)
_y1 = np.arange(0,M/2)
_y2 = np.arange(M/2,0,-1)
_x  = np.concatenate([_x1, _x2])
_y  = np.concatenate([_y1, _y2])
x, y  = np.meshgrid(_x, _y)
kx,ky = x / (dxy * N), y / (dxy * M)
kxy2  = (kx * kx) + (ky * ky)

# let's look at the x grid
normIM=np.zeros((M,N),dtype='uint8')    # make blank image
normIM= cv2.normalize(x,  normIM, 0, 255, cv2.NORM_MINMAX)
normIM=normIM.astype('uint8') # convert int32 to uint8 for display
cv2.imshow('xGrid',normIM)
# now the y grid
normIM= cv2.normalize(y,  normIM, 0, 255, cv2.NORM_MINMAX)
normIM=normIM.astype('uint8') # convert int32 to uint8 for dispaly
cv2.imshow('yGrid',normIM)

# show what's going on
cv2.imshow('raw',cropIM)
print('len(_x1)',len(_x1))
print('len(_x2)',len(_x2));     print()
print('_x1=np.arange(0,N/2)    N =',N,'     N/2 =',N/2)
print(_x1);     print()
print('_x2=np.arange(N/2,0,-1)')
print(_x2);     print()
print('_x  = np.concatenate([_x1, _x2])    len(_x) =',len(_x))
print(_x);      print()
cv2.waitKey(DELAY)      # stop here until image closed

# compute Fourtier Transform at z=0
# let's break this down....
# (A) fftshift shifts the sqrt of the image to the center
print('='*80)
print('Shift the image with the origin in the center')
E0 = np.fft.fft2(np.fft.fftshift(sqrtIM))
print('E0   shape=',E0.shape)
imFFTshift=np.fft.fftshift(sqrtIM)      # shift the squared image
# let's visualize the imFFTshift by converting it into a grayscale image
imFFTshiftInt = imFFTshift.astype('uint8')
# let's normalize it so it uses the full grayscale values (0-255)
normIM=np.zeros((M,N),dtype='uint8')    # make blank image
normIM= cv2.normalize(imFFTshiftInt,  normIM, 0, 255, cv2.NORM_MINMAX)
cv2.imshow('raw',cropIM)
cv2.imshow('sqrt', normIM)

# (B) calculate E0 = the fft2 of the shifted sqrt image
print('E0[10,10] =',E0[10,10]); print() # look at one value
# let's visualize just the real part, normalized to 0-255 so we can see it
realIM=(np.real(E0)).astype(int)
realIM[0,0]=0; # this value was huge, affecting the normalization, so make it 0
realIM=realIM-np.min(realIM)
E0_IM=np.zeros((M,N),dtype='uint8')    # make blank image
E0_IM= cv2.normalize(realIM,  E0_IM, 0, 255, cv2.NORM_MINMAX)
E0_IM=E0_IM.astype('uint8') # convert int32 to uint8 for dispaly
cv2.imshow('FFT',E0_IM)
cv2.imshow('raw',cropIM)
cv2.waitKey(DELAY)      # stop here until image closed

# compute phase aberration
phAbbr   = np.exp(-1j * np.pi * wvlen * z * zScale * kxy2)
output_img = np.fft.ifftshift(np.fft.ifft2(E0 * phAbbr))
realIM=(np.real(phAbbr)) 
phaseIM=np.zeros((M,N),dtype='uint8')    # make blank image
phaseIM= cv2.normalize(realIM,  phaseIM, 0, 255, cv2.NORM_MINMAX)
phaseIM=phaseIM.astype('uint8') # convert int32 to uint8 for dispaly
cv2.imshow('E0',E0_IM)
cv2.imshow('phaseAbb',phaseIM)
cv2.imshow('raw',cropIM)

amp = np.abs(output_img)**2          # output is the complex field, still need to compute intensity via abs(res)**2
amp = np.clip(amp,0,255)        # prevent rollover when converting to 8 bit
ampInt = amp.astype('uint8')
cv2.imshow('reco',ampInt)
cv2.waitKey(DELAY)
cv2.destroyAllWindows()



