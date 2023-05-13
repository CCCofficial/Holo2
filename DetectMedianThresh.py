'''
Detect objects in video and save the dimensions of bounding boxes

1. Resize the video to speed up processing
2. Get the median brightness of the video frames by averaging several (e.g., 20) random video frames
3. For each video frame;
* difference each video frame with the median frame
* blur the difference frame
* apply a fixed threshold to the blurred difference frame
* detect objects 
* save bounding box dimensions of objects with sufficient area

OPERATION
Press 'q' to quit
Use the '+' and '-' keys to change object detect threshold by 1
Old shift while pressing '+' or '-' to change threshould by 10

11/15/2022 Tom Zimmerman CCC, IBM Research 
This work is funded by the National Science Foundation (NSF) grant No. DBI-1548297, Center for Cellular Construction.
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation.
'''

############################## FOR EDUCATIONAL USE ONLY ####################
import numpy as np
import cv2

########## USER SETTINGS ##############################
vid=r'C:\Users\820763897\Videos\microscope\WhiteLightEdit\PlanktonWhiteLight.mp4'    
vid=r'C:\Users\820763897\Videos\microscope\WhiteLightEdit\planktonWhiteLight_960_544.mp4'  
vid=r'C:\Users\820763897\Videos\microscope\Hologram\SFSU_Plankton_Videos\BLE_AMM_6.mp4'
detectFileName='test.csv'

medianFrames=25 # number of random frames to calculate median frame brightness
skipFrames=100  # give video image autobrightness (AGC) time to settle
BLUR=7          # blur differenced images to remove holes in objectes
THRESH=23       # apply threshold to blurred object to create binary detected objects

X_REZ=640; Y_REZ=480; # viewing resolution
MIN_AREA=10     # min area of object detected
VGA=(640,480)       # display resolution
PROCESS_REZ=(320,240)   # processing resolution, video frames reduced in size to speed up processing
    
############# DETECT OUTPUT ##################
detectHeader= 'FRAME,ID,X0,Y0,X1,Y1,XC,YC,AREA,AR,ANGLE'
FRAME=0; ID=1;  X0=2;   Y0=3;   X1=4;   Y1=5;   XC=6;   YC=7; AREA=8; AR=9; ANGLE=10; MAX_COL=11
detectArray=np.empty((0,MAX_COL), dtype='int') # cast as int since most features are int and it simplifies usage

def getMedian(vid,medianFrames,TINY_REZ):
    # Open Video
    print ('openVideo:',vid)
    cap = cv2.VideoCapture(vid)
    maxFrame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('maxFrame',maxFrame)
     
    # Randomly select N frames
    print('calculating median')
    frameIds = skipFrames+ (maxFrame-skipFrames) * np.random.uniform(size=medianFrames)
    frames = [] # Store selected frames in an array
    for fid in frameIds:
        cap.set(cv2.CAP_PROP_POS_FRAMES, fid)
        ret, frame = cap.read()
        colorIM=cv2.resize(frame,TINY_REZ)
        grayIM = cv2.cvtColor(colorIM, cv2.COLOR_BGR2GRAY)
        frames.append(grayIM)
    medianFrame = np.median(frames, axis=0).astype(dtype=np.uint8)     # Calculate the median along the time axis
     
    cap.release()
    return(medianFrame)

def getAR(obj):
    ((xc,yc),(w,h),(angle)) = cv2.minAreaRect(obj)  # get parameters from min area rectangle
    ar=0.0      # initialize aspect ratio as a floating point so calculations are done in floating point
    # calculate aspect ratio (always 1 or greater)
    if w>=h and h>0:
        ar=w/h
    elif w>0:
        ar=h/w
    return(xc,yc,ar,angle)         

######### MAIN PROGRAM #############

print("\n\nUse '+' and '-' keys to change object detect threshold by 1")
print("Hold shift while pressing '+' or '-' to change threshould by 10\n")
# create median frame
medianFrame=getMedian(vid,medianFrames,PROCESS_REZ)

cap = cv2.VideoCapture(vid)
cap.set(cv2.CAP_PROP_POS_FRAMES, skipFrames) # start movie past skipFrames
frameCount=skipFrames
while(cap.isOpened()):
    
    # read key, test for 'q' quit
    key=chr(cv2.waitKey(100) & 0xFF) # pause x msec
    
    if key== 'q':
        break
    elif key=='=':
        THRESH+=1
    elif key=='+':
        THRESH+=10
    elif key=='-' and THRESH>1:
        THRESH-=1
    elif key=='_' and THRESH>11:
        THRESH-=10    
    
    # get image
    ret, colorIM = cap.read()
    if not ret: # check to make sure there was a frame to read
        print('Can not find video or we are all done')
        break
    frameCount+=1
    
    # capture frame, subtract meadian brightness frame, apply binary threshold
    colorIM=cv2.resize(colorIM,PROCESS_REZ)
    grayIM = cv2.cvtColor(colorIM, cv2.COLOR_BGR2GRAY)    # convert color to grayscale image
    diffIM = cv2.absdiff(grayIM, medianFrame)   # Calculate absolute difference of current frame and the median frame           
    blurIM = cv2.blur(diffIM,(BLUR,BLUR))
    ret,binaryIM = cv2.threshold(blurIM,THRESH,255,cv2.THRESH_BINARY) # threshold image to make pixels 0 or 255
    
    # get contours  
    contourList, hierarchy = cv2.findContours(binaryIM, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # all countour points, uses more memory
    
    # draw bounding boxes around objects
    objCount=0      # used as object ID in detectArray
    for objContour in contourList:                  # process all objects in the contourList
        area = int(cv2.contourArea(objContour))     # find obj area        
        if area>MIN_AREA:                           # only detect large objects       
            PO = cv2.boundingRect(objContour)
            x0=PO[0]; y0=PO[1]; x1=x0+PO[2]; y1=y0+PO[3]
            cv2.rectangle(colorIM, (x0,y0), (x1,y1), (0,255,0), 1) # place GREEN rectangle around each object, BGR
            cv2.rectangle(binaryIM, (x0,y0), (x1,y1), 255, 1) # place white rectangle around each object
            (xc,yc,ar,angle)=getAR(objContour)

            # save object parameters in detectArray in format FRAME=0; ID=1;  X0=2;   Y0=3;   X1=4;   Y1=5;   XC=6;   YC=7; CLASS=8; AREA=9; AR=10; ANGLE=11; MAX_COL=12
            parm=np.array([[frameCount,objCount,x0,y0,x1,y1,xc,yc,area,ar,angle]],dtype='int') # create parameter vector (1 x MAX_COL) 
            detectArray=np.append(detectArray,parm,axis=0)  # add parameter vector to bottom of detectArray, axis=0 means add row
            objCount+=1                                     # indicate processed an object
    print('thresh:',THRESH,'frame:',frameCount,'all objects:',len(contourList),'big objects:',objCount)

    # shows results
    cv2.imshow('colorIM', cv2.resize(colorIM,VGA))      # display image
    cv2.imshow('blurIM', cv2.resize(blurIM,VGA))        # display thresh image
    cv2.imshow('diffIM', cv2.resize(diffIM,VGA))        # display thresh image
    cv2.imshow('medianFrame', cv2.resize(medianFrame,VGA))        # display thresh image
    cv2.imshow('binaryIM', cv2.resize(binaryIM,VGA))    # display thresh image

if frameCount>0:
    print('Done with video. Saving feature file and exiting program')
    np.savetxt(detectFileName,detectArray,header=detectHeader,delimiter=',', fmt='%d')
    cap.release()
else:
    print('Count not open video',vid)
cv2.destroyAllWindows()








