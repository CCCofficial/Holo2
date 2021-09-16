"""
findZ
Manually find reconsturction Z and save reconstructed image and z value in image name
Designed for file format 'alg_3_4360.jpg'. Change line 96 if different format.

V10 9.13.21 Added startswith for Mac hidden files
V9  8.21.21 Prevent Z from going negative, added instructions
v8  8.21.21 Fixed rollover error on reconstruction using clipping
V7  6.05.21 saves the reco image as foo_1_4000_reco.jpg
V6  2.23.21 image format= did_13_3940.jpg where 13 is image number, Z in um, if z=0, no focus is provided

Use SPACE BAR to save z in file name.
Use 'x' to skip file
Use 'q' to quit
"""
import numpy as np
import cv2
from os import listdir,rename,getcwd
from os.path import isfile, join
from matplotlib import pyplot as plt

################## SETTINGS ################
defaultZ=3000       # if z is not known
zStep = 20          # how many Z values to traverse at a time.
dxy   = 1.4e-6      # imager pixel size in meters.
wvlen = 650.0e-9    # red laser wavelength (meters)
zScale=1e-6         # convert z units to microns 
DISPLAY_REZ=(800,800)  

dirIn = r'\rawImage\\'
dirOut = r'\recoImage\\'
imageNamePrefix='testImage'        # used when saving images
maxContrast=0
bestZ=0
################# FUNCTIONS #################

def recoFrame(cropIM, z):
    #make even coordinates
    (yRez,xRez)=cropIM.shape
    if (xRez%2)==1:
        xRez-=1
    if (yRez%2)==1:
        yRez-=1
    cropIM=cropIM[0:yRez,0:xRez]
    res = propagate(np.sqrt(cropIM), wvlen, z, dxy)	 #calculate wavefront at z
    amp = np.abs(res)**2          # output is the complex field, still need to compute intensity via abs(res)**2
    amp = np.clip(amp,0,255)        # prevent rollover when converting to 8 bit
    ampInt = amp.astype('uint8')
    return(ampInt)

def propagate(input_img, wvlen, zdist, dxy):
    M, N = input_img.shape # get image size, rows M, columns N, they must be even numbers!

    # prepare grid in frequency space with origin at 0,0
    _x1 = np.arange(0,N/2)
    _x2 = np.arange(N/2,0,-1)
    _y1 = np.arange(0,M/2)
    _y2 = np.arange(M/2,0,-1)
    _x  = np.concatenate([_x1, _x2])
    _y  = np.concatenate([_y1, _y2])
    x, y  = np.meshgrid(_x, _y)
    kx,ky = x / (dxy * N), y / (dxy * M)
    kxy2  = (kx * kx) + (ky * ky)

    # compute FT at z=0
    E0 = np.fft.fft2(np.fft.fftshift(input_img))

    # compute phase aberration
    _ph_abbr   = np.exp(-1j * np.pi * wvlen * zdist * kxy2)
    output_img = np.fft.ifftshift(np.fft.ifft2(E0 * _ph_abbr))
    return output_img

def directions():
    print('='*30,'DIRECTIONS','='*30)
    print('Click on image to enable key commands')
    print('Press "+" and "-" keys to change reconstruction z in 20 um steps')
    print('Hold "shift" while pressing "+" or "-" keys to change z in 200 um steps')
    print('Press SPACE BAR to save z in file name')
    print('Press "x" to skip file')
    print('Press "q" to quit program')
    print('='*73)
    print()

def plotLine(im,z):
    global maxContrast,bestZ
    
    (yMax,xMax)=im.shape 
    midLine=int(yMax/2)
    iMin=min(im[midLine,:])
    iMax=max(im[midLine,:])
    contrast=int(iMax-iMin)
    if contrast>maxContrast:
        maxContrast=contrast
        bestZ=z
    plt.clf()
    plt.title('Contrast ='+str(contrast)+' ('+ str(maxContrast)+ ')   z =' + str(z) + ' ('+str(bestZ)+')')
    plt.xlabel('X')
    plt.ylabel('Intensity')
    plt.ylim([0, 255])          # limit y range
    plt.xlim([0, xMax])         # limit x range
    plt.plot(im[midLine,:])
    p1=(0,midLine)
    p2=(xMax,midLine)
    return(p1,p2)
    
##############  MAIN  ##############
directions() # print directions
# find files in directory
cwd=getcwd()
plt.ion()
plt.figure()
            
files = [f for f in listdir(cwd+dirIn) if isfile(join(cwd+dirIn, f)) if not f.startswith('.')] # added startswitch for Mac hidden files
startIndex=0
z=defaultZ
lastZ=0
for i in range(startIndex,len(files)):
    maxContrast=0
    bestZ=0
    p1=(0,0); p2=(0,0);
    fileName=files[i]
    print('Processing:',fileName)
    
    # create fileIndex from fileName, file format 'alg_3_4360.jpg'
    a=fileName.split('_')
    imageNumber=int(a[1]) # if file format '3_4360.jpg', change a[1] to a[0]
    
    # get image
    im = cv2.imread(cwd + dirIn + fileName, 0) #Read the image as grayscale
   
    count=0
    done=False
    end=False
    reject=False
    while done==False and end==False:
        ampIM = recoFrame(im, z*zScale)
        cv2.imshow('reco',cv2.resize(ampIM,DISPLAY_REZ))
        cv2.imshow('raw',cv2.resize(im,DISPLAY_REZ))
        if z!=lastZ:
            (p1,p2)=plotLine(ampIM,z)
            lastZ=z
        cv2.line(ampIM,p1,p2,255,1)
        cv2.imshow('reco',cv2.resize(ampIM,DISPLAY_REZ))
        cv2.imshow('raw',cv2.resize(im,DISPLAY_REZ))
        key=cv2.waitKey(1)
        if key==ord(' '): #space bar SAVE GOOD X
            done=True
        elif key==ord('='): 
            z+=zStep
            print(z,end=',')
        elif key==ord('+'): 
            z+=zStep*10
            print(z,end=',')
        elif key==ord('-'):
            z-=zStep
            if z<0:
                z=0
                print('MIN VALUE',end=',')
            print(z,end=',')
        elif key==ord('_'): 
            z-=zStep*10
            if z<0:
                z=0
                print('MIN VALUE',end=',')
            print(z,end=',')
        elif key== ord('q'):
            end=True
        elif key==ord('x'):
            done=True
            reject=True
        
    if end==True:
        break
    elif reject==True:
        pass
    elif done==True:
        newName=imageNamePrefix+'_'+str(imageNumber)+'_'+str(z)+'_reco.jpg'
        cv2.imwrite(cwd+dirOut+newName,ampIM)
        print()
        print('Saved:',newName)
        print()
        
print('Quit requested so closing window and ending program, bye!')
cv2.destroyAllWindows()
