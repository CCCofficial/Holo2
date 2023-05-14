# Run a stack of images through a 0 and 90 deg Gabor Filter
# Select the image with the highest Gabor value
# Tom Zimmerman, IBM Research-Almaden, CCC, 5.1.23

import numpy as np
from scipy import ndimage as ndi
from skimage.filters import gabor_kernel
from os.path import isfile, join
from os import listdir
import cv2
from matplotlib import pyplot as plt
import math


rawImageDir=r'C5_Z5\\'     
savePlotFileName=r'C5.png'

def convolve(image, kernel):
    feat = np.zeros((len(kernel)), dtype=np.double)
    filtered = ndi.convolve(image, kernel, mode='wrap')
    feat = filtered.var()
    return feat

################## MAIN ##########################

# prepare filter kernels
theta=0
angle = theta / 4. * np.pi
sigma=1 # 4,9,12
frequency=0.35 #0.125, 0.25,0.35,0.50
kernel0 = np.real(gabor_kernel(frequency, theta=angle,sigma_x=sigma, sigma_y=sigma))
theta=90
angle = theta / 4. * np.pi
kernel90 = np.real(gabor_kernel(frequency, theta=angle,sigma_x=sigma, sigma_y=sigma))

# process Z stack
files = [f for f in listdir(rawImageDir) if isfile(join(rawImageDir, f))]
gvar=np.zeros((len(files),2))
maxGabor=0
bestFocus=0
for i in range(len(files)):
    fileName=rawImageDir+str(i)+'.jpg'
    print(fileName)
    grayIM=cv2.imread(fileName,0)        # load as grayscale
    tinyIM=cv2.resize(grayIM, (640,480))    # make image smaller for faster processing
    
    gaborValue0=convolve(tinyIM, kernel0)
    gaborValue90=convolve(tinyIM, kernel90)
    gaborValue=math.sqrt(gaborValue0**2+gaborValue90**2)
    gvar[i]=gaborValue
    if gaborValue>maxGabor:
        maxGabor=gaborValue
        bestFocus=i
    
# plot and save Gabor plot
plt.plot(gvar)
plt.xlabel('image number')
plt.ylabel('gabor filter value')
plt.title("Gabor Filter on Images  Best="+str(bestFocus))
plt.savefig(savePlotFileName)
plt.show()

print('bestFocusImage',bestFocus)



