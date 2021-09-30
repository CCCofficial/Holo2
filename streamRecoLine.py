'''

Interactive Holographic Reconstruction with Tkinter Interface with Line Contrast Display

V5 9.01.21 Changed call from vc3 to reco (renamed)
V4 3.01.21 Removed unused buttons, added instructions, uses vc3 support function file
V3 2.23.21 Changed Z_SCALE to be in units of 10 um 
V1 2.09.21

For Python control of camera values, see https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-set

For Pi Control of camera values use PuTTY;
     type login, root, (password) root, control-J (for carriage return), cd bin, camera-ctl 
Button Fuctions
===============
Frame: Select frame to display
Crop: Crops section of image to reconstruction, smaller makes for faster reconstruction
Z: Change reconstruction height (distance between object and image sensor)
Display: Change size of reconstruction display (doesn't effect reconstruction or save image size)
SavePic: Saves reconstructed cropped image, image format= foo_23_100_200_300_holo.jpg and foo_23_100_200_3000_raw.jpg where:
        "foo" is from the video name
        "23" is frame number
        "100" and "200" are the x,y location of the center of the cropped image from the full frame image (1920x1080)
        "3000" is the z value (distance between object and image sensor (in microns)
        "raw" is the original cropped holographic image
        "holo" is the image reconstructed at distance z (3000um in this example)
Center: To center cropped image, press "Center", place cursor over center object, then left click
To end program, click 'X' in top right of button panel

General Use Guide
=================
Put your video file location in 'vid=' below.
Use Center to find an object of interest
Use Crop to select a cropping size that captures the object and it's fringes but not much else to speed up reconstruction time
Use Z+10 and Z-10 to get a coarse "focus" of the object
Use Z+1 and Z-1 to get a fine "focus" of the object
Use x+10,x-10,y+10,y-10 to change line location
When you are happy with the image, click "SavePic" to save the image. The program will automatically save the raw and reconstructed images along with video name, frame number, crop location and reconstruction Z embeded in the image name.
Use Frame to move around the frames in the movie

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

vid=r'\rawVideo\M6.mp4'     # put your video location here, must be mp4, use ffmpeg to convert microscope .h264 to .mp4
imageNamePrefix='M6'        # used when saving images
rawImageDir=r'\rawImage\\'   # directory where saved images are stored
recoImageDir=r'\recoImage\\'   # directory where saved images are stored
    
###################### INITIALIZE GLOBAL VALUES #############################
MICROSCOPE_CAM=0        # location of microscope as web cam (usually 0 or 1)
xRez=1920; yRez=1080;   # video resolution
displayScale=1          # scale display output
window=[0,yRez,0,xRez]
frameCount=1            # current frame being examined
Z=5400                  # starting Z location (x10um)
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
LINE_LEN=100            # length of conrast plotting line
maxContrast=0           # result of contrast calculation
bestZ=0
# Button names. Some are left blank for future functions.
names = [
    ("x -10"),
    ("y -10"),
    ("x +10"),
    ("y +10"),
    ("Crop -10"),
    ("Crop -1"),
    ("Crop +1"),
    ("Crop +10"),
    ("Z -10"),
    ("Z -1"),
    ("Z +1"),
    ("Z +10"),
    (" "), 
    (" "),
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
    print('==========USER GUIDE ===================')
    print('Use Center to find an object of interest')
    print('Use Crop to select a cropping size')
    print('Use Z+10 and Z-10 to get a coarse "focus" of the object')
    print('Use Z+1 and Z-1 to get a fine "focus" of the object')
    print('Click "SavePic" to save raw and reco images')
    print('Use Frame to change movie frame')
    print('Hit the X in the top right corner to end program')
    print('========================================')
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
    
    if 'mp4' in vid:
        name=vid[:-4]
    elif 'h264' in vid: # should not be using h264 video format, convert to mp4
        print('WARNING: Should be using mp4 video, not h264 format')
        name=vid[:-5]
    else:
        name=vid

    # save holo image
    print()
    imageName=imageNamePrefix+'_'+str(imageCount)+'_'+str(Z)+'_reco.jpg'
    cv2.imwrite(cwd+recoImageDir+imageName,holoIM)
    print ('Saved image',imageName)
    
    # save raw cropped image
    imageName=imageNamePrefix+'_'+str(imageCount)+'_'+str(Z)+'_raw.jpg'
    cv2.imwrite(cwd+rawImageDir+imageName,cropIM)
    print ('Saved image',imageName)
    imageCount+=1 # increment for next saved images
    v.set(2)  # set choice to "+1 Frame" so user won't be confused by SavePic being on
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
    global x,y,displayScale,Z,CROP,getCenter,savePic,bkgState,bkgIM,maxContrast

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
    elif 'x' in but:
        x+=increment
        maxContrast=0
        bestZ=0
    elif 'y' in but:
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
    
    updateStatusDisplay()
    processImage()
    return

def doLine(im):
    (r,c)=im.shape
    p1=(x,y)
    p2=(x,y+LINE_LEN)
    cv2.line(im,p1,p2,255,1)
    return(im)

def plotLineIntensity(im):
    global maxContrast,bestZ,x,y

    (yCropRez,xCropRez)=im.shape
    x=clamp(x,0,xCropRez-1)
    y=clamp(y,0,yCropRez-1)
    iMin=min(im[y:y+LINE_LEN,x])
    iMax=max(im[y:y+LINE_LEN,x])
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
    plt.xlim([0, LINE_LEN])         # limit x range
    plt.plot(im[y:y+LINE_LEN,x])
    
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
if 'mp4' not in vid:    # can only process mp4 videos!
    goodVideo=0
    
if goodVideo:
    root = tk.Tk()
    v = tk.IntVar()
    v.set(2)            # set choice to "+1 Frame"

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
    print('Could not open video file:',vid)
    print("Can't find file or not an mp4 video")
