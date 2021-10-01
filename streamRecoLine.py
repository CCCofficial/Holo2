'''
Interactive Holographic Reconstruction with Tkinter Interface with Line Contrast Display

V7 10.01.21 Added change line length, fixed Display size bug, removed all vid, MP4 and Frame reference, removed all image directory (now puts in same directory as running program) 
V6 09.30.21 Removed Frame, video link, cwd (working directory) from code

For Python control of camera values, see https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-set

For Pi Control of camera values use PuTTY;
     type login, root, (password) root, control-J (for carriage return), cd bin, camera-ctl
     
Button Fuctions
===============
x,y: Moves the line to measure constrast in the reconstructed cropped image
Line: Change the length of the line that measures constrast
Crop: Crops section of image to reconstruction, smaller makes for faster reconstruction
Z: Change reconstruction height (distance between object and image sensor)
Display: Change size of reconstruction display (doesn't effect reconstruction or save image size)
SavePic: Saves reconstructed cropped image, image format= 2_holo.jpg and 2_3000_raw.jpg where:
        "2" is the image number (starts with 0 every time the program runs)frame number
        "3000" is the z value (distance between object and image sensor (in microns)
        "raw" is the original cropped holographic image
        "holo" is the image reconstructed at distance z (3000um in this example)
Center: To center cropped image, press "Center", place cursor over center object, then left click
To end program, click 'X' in top right of button panel

General Use Guide
=================
Use x+10,x-10,y+10,y-10 to change line location
Use Center to find an object of interest
Use Crop to select a cropping size that captures the object and it's fringes but not much else to speed up reconstruction time
Use Z+10 and Z-10 to get a coarse "focus" of the object
Use Z+1 and Z-1 to get a fine "focus" of the object
When you are happy with the image, click "SavePic" to save the image. The program will automatically save the raw and reconstructed images in the same directory the program is running in.
Warning, each time you start the program, saved images start with 0 so it might erase previous images if the Z happens to be the same.

Thomas Zimmerman, IBM Research-Almaden
Holgraphic Reconstruction Algorithms by Nick Antipac, UC Berkeley and  Daniel Elnatan, UCSF
This work is funded by the National Science Foundation (NSF) grant No. DBI-1548297, Center for Cellular Construction.
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation. 
'''

import tkinter as tk
import reco                 # performs reconstruction
import cv2
import numpy as np
from matplotlib import pyplot as plt

    
###################### INITIALIZE GLOBAL VALUES #############################
MICROSCOPE_CAM=0        # location of microscope as web cam (usually 0 or 1)
xRez=1920; yRez=1080;   # video resolution
displayScale=1          # scale display output
window=[0,yRez,0,xRez]
frameCount=1            # current frame being examined
Z=4000                  # starting Z location (x10um)
CROP=25                 # starting crop size
BUTTON_WIDTH=10         # button display width
WINDOW_SCALE=10         # window size increment
Z_SCALE=1e-6            # convert z units to microns 
FULL_SCALE=2            # reduce full scale image by this factor so it fits in window
xc=1082; yc=468;        # initial center of crop window
getCenter=False         # flag that when sets xc,y, to mouse location on click
savePic=False           # save pic of reconstruction when flag set
imageCount=0            # used when saving image
x=410                   # starting location of line that displays contrast plot
y=150
lineLen=200             # length of contrast plotting line
maxContrast=0           # result of contrast calculation
bestZ=0
# Button names. Some are left blank for future functions.
names = [
    ("X -10"),
    ("X +10"),
    ("Y -10"),
    ("Y +10"),
    ("Crop -10"),
    ("Crop -1"),
    ("Crop +1"),
    ("Crop +10"),
    ("Z -10"),
    ("Z -1"),
    ("Z +1"),
    ("Z +10"),
    ("Line -10"), 
    ("Line +10"),
    ("Display -1"),
    ("Display +1"), 
    (" "), 
    (" "),
    ("SavePic"),
    ("Center")
]

####################### PROCEDURES ##########################################
def doc():
    print()
    print('==================  USER GUIDE  ========================')
    print('Use X and Y to move constrast line in crop window')
    print('Use Line to change the length of the vertical line')
    print('Use Center to find an object of interest')
    print('Use Crop to select a cropping size')
    print('Use Z+10 and Z-10 to get a coarse "focus" of the object')
    print('Use Z+1 and Z-1 to get a fine "focus" of the object')
    print('Click "SavePic" to save raw and reco images')
    print('Hit the X in the top right corner to end program')
    print('========================================================')
    print()
    
def doMouse(event,x,y,flags,param):
    global getCenter,xc,yc

    processImage()
    if getCenter and event == cv2.EVENT_LBUTTONDOWN:
        xc,yc = x*FULL_SCALE,y*FULL_SCALE # compensate for full scale scaling
        processImage()
    return

def updateStatusDisplay():
    textOut=' x='+ str(x) + '    y='+ str(y) + '    Crop=' + str(CROP) + '    Z=' + str(Z) + '    Display=' + str(displayScale)+'   '
    tk.Label(root, text=textOut,bg="yellow",justify = tk.LEFT).grid(row=0,column=0,columnspan=4)
    return

def savePicture(holoIM,cropIM):
    global v,imageCount

    # save holo image
    print()
    imageName=str(imageCount)+'_'+str(Z)+'_reco.jpg'
    cv2.imwrite(imageName,holoIM)
    print ('Saved image',imageName)
    
    # save raw cropped image
    imageName=str(imageCount)+'_'+str(Z)+'_raw.jpg'
    cv2.imwrite(imageName,cropIM)
    print ('Saved image',imageName)
    imageCount+=1       # increment for next saved images
    v.set(8)            # set choice to "Z -10" so user won't be confused by 'savePic' still selected
    return
    
def updateWindow():
    global window
    x0=xc-(WINDOW_SCALE*CROP)
    x1=xc+(WINDOW_SCALE*CROP)
    y0=yc-(WINDOW_SCALE*CROP)
    y1=yc+(WINDOW_SCALE*CROP)

    x0=clamp(x0,0,xRez)
    x1=clamp(x1,x0,xRez)
    y0=clamp(y0,0,yRez)
    y1=clamp(y1,y0,yRez)

    window=[y0,y1,x0,x1]
    return

def doButton():
    global x,y,displayScale,Z,CROP,getCenter,savePic,bkgState,bkgIM,maxContrast,lineLen

    getCenter=False #clear flag in case button is not Center, allows multiple centers until another button pushed
    val=v.get()
    but=names[val]

    increment=0
    if "-10" in but:
        increment=-10
    elif "+10" in but:
        increment=10
    elif "-1" in but:
        increment=-1
    elif "+1" in but:
        increment=1

    if 'Center' in but:
        getCenter=True  # this flag tells doCenter to update xc,yc
    elif 'SavePic' in but:
        savePic=True  # flag indicates picture capture requested
    elif 'X' in but:
        x+=increment
        maxContrast=0
        bestZ=0
    elif 'Y' in but:
        y+=increment
        maxContrast=0
        bestZ=0
    elif 'Z' in but:
        Z+=increment*20 # increment in steps of 20 um
        if Z<1:
            Z=1
    elif 'Display' in but:
        displayScale+=increment
        if displayScale<1:
            displayScale=1
    elif 'Crop' in but:
        CROP+=increment
        if CROP<1:
           CROP=1
    elif 'Line' in but:
        lineLen+=increment
        if lineLen<1:
           lineLen=1
    
    updateStatusDisplay()
    processImage()
    return

def doLine(im):
    (r,c)=im.shape
    p1=(x,y)
    p2=(x,y+lineLen)
    cv2.line(im,p1,p2,255,1)
    return(im)

def plotLineIntensity(im):
    global maxContrast,bestZ,x,y

    (yCropRez,xCropRez)=im.shape
    x=clamp(x,0,xCropRez-1)
    y=clamp(y,0,yCropRez-1)
    iMin=min(im[y:y+lineLen,x])
    iMax=max(im[y:y+lineLen,x])
    contrast=(iMax-iMin)/(iMax+iMin)
    if (iMax-iMin)>(iMax+iMin):             # debugging for I once observed contrast>1 !
        print('Contrast Error','iMin',iMin,'iMax',iMax)
    contrast=round(contrast,2)
    if contrast>maxContrast:
        maxContrast=contrast
        bestZ=Z
    plt.clf()
    plt.title('Contrast ='+str(contrast)+' ('+ str(maxContrast)+ ')   z =' + str(Z) + ' ('+str(bestZ)+')')
    plt.xlabel('y')
    plt.ylabel('Intensity')
    plt.ylim([0, 255])              # limit y range
    plt.xlim([0, lineLen])         # limit x range
    plt.plot(im[y:y+lineLen,x])
    
def processImage():
    global savePic
    
    updateWindow()
    ret, rawIM = cap.read()
    grayIM = cv2.cvtColor(rawIM, cv2.COLOR_BGR2GRAY)
    cropIM=grayIM[window[0]:window[1],window[2]:window[3]] # crop window of image
    recoIM=reco.recoFrame(cropIM,Z*Z_SCALE)
    plotLineIntensity(recoIM)
    recoIM=doLine(recoIM)
    rescaleRecoIM=cv2.resize(recoIM,None,fx=displayScale,fy=displayScale)
    rescaleFullIM=cv2.resize(grayIM,None,fx=1.0/FULL_SCALE,fy=1.0/FULL_SCALE)

    cv2.imshow('Crop Reconstructed',rescaleRecoIM)
    cv2.imshow('Full Image',rescaleFullIM)
    cv2.waitKey(10)

    if savePic==True:
        savePicture(recoIM,cropIM) # save reconstructed and cropped raw image
        savePic=False   # reset flag so it ony does once per mouse click
    return

################################ MAIN ##################################
clamp = lambda value, minv, maxv: max(min(value, maxv), minv)

doc() # print user guide
plt.ion()
plt.figure()    
cap = cv2.VideoCapture(MICROSCOPE_CAM) # select external web camera (microscope)
cap.set(3, 1920); cap.set(4, 1080); # set to 1080p resolution
goodVideo, frame = cap.read()

count=0    
if goodVideo:
    root = tk.Tk()
    v = tk.IntVar()
    v.set(8)            # set initial choice to "Z -10"

    root.title("Holographic Reconstruction")
    updateStatusDisplay()

    for val, txt in enumerate(names):
        r=int(1+val/4)
        c=int(val%4)
        tk.Radiobutton(root, text=txt,padx = 1, variable=v,width=BUTTON_WIDTH,command=doButton,indicatoron=0,value=val).grid(row=r,column=c)

    processImage()
    cv2.setMouseCallback('Full Image',doMouse)
    MAX_FRAME=32000
    
    try:
        while True:
            processImage()
            root.update()
    except:
        pass
    cap.release()
    cv2.destroyAllWindows()
    plt.close()
    print ('Ending program, bye!')
else:
    print('Camera not found on port',MICROSCOPE_CAM)
    
